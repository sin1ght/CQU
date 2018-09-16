from screen.output import Output
from configparser import ConfigParser,NoOptionError,NoSectionError
from core.baseclass import BaseManager
from core.sakai.manager import Manager as SakaiManager
from core.jww.manager import Manager as JwwManager
from core.exceptions import LoginException


class Manager(BaseManager):

    def __init__(self):
        super(Manager, self).__init__()
        self.cmd_str='CQU'
        self._config_path='./conf/config.ini'
        self._config=ConfigParser()
        self._config.read(self._config_path,encoding='utf8')
        self._cache={}

    def config(self,args):
        '''
        :command:
        :doc:查看或设置登录密码
        :usage:
        config get jww.username
        config set jww.password=123
        config 查看所有配置信息
        '''
        if len(args)==0:
            #config
            with open(self._config_path,'r',encoding='utf8') as f:
                print(f.read())
        else:
            if args[0]=='get':
                #config get jww.username
                keys=args[1].split('.')
                try:
                    print(self._config.get(keys[0],keys[1]))
                except NoSectionError:
                    Output.error("不存在类别%s" % keys[0])
                except NoOptionError:
                    Output.error("类别%s不存在字段%s"%(keys[0],keys[1]))
            if args[0]=='set':
                #config set jww.username=123456
                k,v=args[1].split('=')
                keys=k.split('.')
                if self._config.has_section(keys[0]):
                    if self._config.has_option(keys[0],keys[1]):
                        self._config.set(keys[0],keys[1],v)
                        with open(self._config_path, 'w', encoding='utf8') as f:
                            self._config.write(f)
                    else:
                        Output.error("类别%s不存在字段%s" % (keys[0], keys[1]))
                else:
                    Output.error("不存在类别%s" % keys[0])

    def sakai(self,args):
        '''
        :command:
        :doc:进入sakai系统
        :usage:sakai
        '''
        try:
            if self._cache.__contains__('sakai'):
                self._cache['sakai'].running=True
                self._cache['sakai'].run()
            else:
                s = SakaiManager.login(self._config.get('com_login', 'username'),
                                       self._config.get('com_login', 'password'))
                sakai = SakaiManager(s)
                self._cache['sakai'] = sakai
                sakai.run()
        except LoginException:
            Output.error("账号或密码错误")

    def jww(self,args):
        '''
        :command:
        :doc:进入教务网系统
        :usage:jww
        '''
        try:
            if self._cache.__contains__('jww'):
                self._cache['jww'].running=True
                self._cache['jww'].run()
            else:
                s = JwwManager.login(self._config.get('jww', 'username'),
                                       self._config.get('jww', 'password'))
                jww = JwwManager(s)
                self._cache['jww'] = jww
                jww.run()
        except LoginException:
            Output.error("账号或密码错误")


if __name__ == '__main__':
    Output.banner()
    CQU=Manager()
    CQU.run()
