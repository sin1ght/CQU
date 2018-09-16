from core.baseclass import BaseManager
from utils.md5 import md5
import requests
from core.exceptions import LoginException
from pyquery import PyQuery as pq
from screen.output import Output
import re
from core.config import PLUGIN_DIR
import os
import importlib

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0",
}


class Manager(BaseManager):
    jww_url = "http://202.202.1.176:8080"

    def __init__(self,session):
        super(Manager, self).__init__()
        self.cmd_str='jww'
        self._session=session
        self._plugin_dir=os.path.join(PLUGIN_DIR,'jww')

    def score(self,args):
        '''
        :command:
        :doc:根据学年,学期查看自己成绩
        :usage:socre 2017[学年] 2[学期(1,2)]
        '''
        if len(args)==2:
            args[1]=int(args[1])-1
            if int(args[1]) not in [0,1]:
                Output.error('请输入正确的的学期')
                return

            url = Manager.jww_url + '/xscj/Stu_MyScore_rpt.aspx'
            data = {
                'btn_search': '检索',
                'sel_xn': args[0],  # 学年
                'sel_xq': args[1],  # 学期 0 第一学期 1 第二学期
                'SelXNXQ': 2,  # 0 入学以来 1 学年 2 学期
                'SJ': 1,  # 1 有效成绩 0 原始成绩
                'zfx_flag': 0,  # 0 主修 1 辅修
                'zxf': 0
            }
            r = self._session.post(url, headers=headers, data=data)
            if re.search('id=\'ID_Table\'',r.text,re.I):
                d=pq(r.text)
                subjects=[]
                for item in d('#ID_Table tr').items():
                    tds=item.children('td')
                    name=tds.eq(1).text()
                    credit=tds.eq(2).text() # 学分
                    category=tds.eq(3).text()
                    mark = tds.eq(6).text() #成绩
                    subjects.append([name,credit,category,mark])
                Output.print_score(subjects)
            else:
                Output.error('请输入正确的的学年')
        else:
            self.usage(self.score)

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

    @staticmethod
    def login(stuid,password):
        s=requests.Session()
        encode = md5(stuid + md5(password)[:30].upper() + '10611')[:30].upper()
        res =s.post(Manager.jww_url + '/_data/index_login.aspx', data={
            '__VIEWSTATEGENERATOR': 'CAA0A5A7',
            'Sel_Type': 'STU',
            'txt_dsdsdsdjkjkjc': stuid,
            'efdfdfuuyyuuckjg': encode
        }, headers=headers)
        if "正在加载权限数据" in res.text:
            return s
        else:
            raise LoginException()


if __name__ == '__main__':

    pass


