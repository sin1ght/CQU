from .meteclass import ManagerMetaClass
from screen.output import Output
import re
from utils.colors import Fore


class BaseManager(metaclass=ManagerMetaClass):
    def __init__(self):
        self.cmd_str='' #命令行提示符
        self.cur_cmd = ''  # 当前命令
        self.running=True #是否正在运行

    def __input(self):
        ''' 获取用户输入'''
        self.cur_cmd=str(input(Fore.YELLOW+"{} > ".format(self.cmd_str)+Fore.END)).strip()
        while not self.cur_cmd:
            self.cur_cmd = str(input(Fore.YELLOW+"{} > ".format(self.cmd_str)+Fore.END)).strip()
        self.__parse_cmd()

    def __parse_cmd(self):
        '''处理命令'''
        cmds=self.cur_cmd.split(' ')
        if hasattr(self,cmds[0]):
            try:
                getattr(self, cmds[0])(cmds[1:])
            except Exception:
                pass
        else:
            Output.error("未知的命令")

    def run(self):
        while self.running:
            self.__input()

    def help(self,args):
        '''
        :command:
        :doc:显示帮助信息
        '''
        if len(args)>0:
            if hasattr(self,args[0]):
                self.usage(getattr(self,args[0]))
            else:
                Output.error('未知的命令')
        else:
            Output.print_help(self.commands)

    def exit(self,args):
        '''
        :command:
        :doc:退出
        :usage:exit
        '''
        self.running=False

    def usage(self,func):
        try:
            usage = re.search(':usage:(.*)', func.__doc__,re.S).group(1)
            Output.info('[usage]\r\n' + usage)
        except Exception:
            pass