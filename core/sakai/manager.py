from core.baseclass import BaseManager
import requests
from pyquery import PyQuery as pq
from core.exceptions import LoginException
import re
import datetime
from screen.output import Output
from threading import Thread,Lock
import os
import importlib
from core.config import PLUGIN_DIR


headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0",
}


class Manager(BaseManager):
    def __init__(self,session):
        super(Manager, self).__init__()
        self.cmd_str='sakai'
        self._session=session
        self._cache={}
        self._lock=Lock()
        self._plugin_dir=os.path.join(PLUGIN_DIR,'sakai')

    def homework(self,args):
        '''
        :command:
        :doc:查看本学期课程未完成作业
        :usage:homework
        '''
        first=False
        if self._cache.__contains__('subjects'):
            subjects = self._cache['subjects']
        else:
            subjects = []

            subject_url="http://sakai.cqu.edu.cn/portal"
            r=self._session.get(subject_url,headers=headers)
            doc=pq(r.text)
            for item in doc('#topnav li a[role=menuitem]').filter('a[title]').items():
                name=item.attr['title'].split(':')[1]
                if name.startswith(str(datetime.datetime.now().year)):
                    herf=item.attr['href']
                    subjects.append({
                        'name':name,
                        'url':herf
                    })

            for item in doc('#otherSiteList li a[title]').items():
                name = item.attr['title']
                if name.startswith(str(datetime.datetime.now().year)):
                    herf=item.attr['href']
                    subjects.append({
                        'name':name,
                        'url':herf
                    })
            first=True

        threads=[]
        for item in subjects:
            t=Thread(target=self.__fetch_homework,args=(item,))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        if first:
            #第一次 则添加缓存
            self._cache['subjects'] = subjects

    def plugin(self,args):
        '''
        :command:
        :doc:查看使用插件
        :usage:
        plugin 显示可用插件
        plugin test[插件名称] args[插件参数]
        plugin help test[插件名称] 查看插件使用方式
        '''
        if len(args)>0:
            if args[0]=='help':
                try:
                    m = importlib.import_module('plugin.jww.{}'.format(args[1]))
                    usage = re.search(':usage:(.*)', m.__doc__, re.S).group(1)
                    Output.info('[usage]\r\n' + usage)
                except ModuleNotFoundError:
                    Output.error('未知的插件')
            else:
                try:
                    m = importlib.import_module('plugin.jww.{}'.format(args[0]))
                    m.run(self._session, args[1:])
                except ModuleNotFoundError:
                    Output.error('未知的插件')
        else:
            commands=[]
            for file in os.listdir(self._plugin_dir):
                file=os.path.splitext(file)[0]
                if not file.startswith('__'):
                    m = importlib.import_module('plugin.jww.{}'.format(file))
                    desc=re.search(':desc:(.*)',m.__doc__).group(1)
                    commands.append({'name':file,'doc':desc})
            Output.print_plugin(commands)

    def __fetch_homework(self,subject):

        if not self._cache.__contains__('subjects'):
            doc=pq(self._session.get(subject['url'],headers=headers).text)
            homework_url=doc('a[title=在线发布、提交和批改作业]').attr['href']

            if homework_url:
                #有些课程没有作业这个功能
                d1=pq(self._session.get(homework_url,headers=headers).text)
                homework_url=d1('iframe').attr['src']
            else:
                return

        else:
            d1 = pq(self._session.get(subject['url'], headers=headers).text)
            homework_url = d1('iframe').attr['src']

        if homework_url:
            # 有些课程没有作业
            d = pq(self._session.get(homework_url, headers=headers).text)

            homeworks = []
            for item in d('table tr').filter(lambda i: i > 0).items():
                status = item.find('td[headers=status]').text().strip()
                if status == '尚未提交':
                    name = item.find('td[headers=title]').text().strip()
                    start_time = item.find('td[headers=openDate]').text().strip()
                    end_time = item.find('td[headers=dueDate]').text().strip()
                    homeworks.append({'name': name, 'start': start_time, 'end': end_time})

            if len(homeworks) > 0:
                subject['homeworks'] = homeworks
                self._lock.acquire()
                Output.print_homework(subject)
                self._lock.release()

    @staticmethod
    def login(username,password):
        s=requests.Session()
        url="http://authserver.cqu.edu.cn/authserver/login?service=http://sakai.cqu.edu.cn/portal/login"
        doc = pq(s.get(url=url,headers=headers).text)
        lt=doc('input[name=lt]').val()
        execution=doc('input[name=execution]').val()

        data={
            "username":username,
            "password":password,
            "execution":execution,
            "lt":lt,
            "dllt":"=userNamePasswordLogin",
            "_eventId":"submit",
            "rmShown":1
        }
        r=s.post(url=url,headers=headers,data=data)
        if re.search('logout',r.text,re.I):
            return s
        else:
            raise LoginException()


if __name__=="__main__":
    pass
