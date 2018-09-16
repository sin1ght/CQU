from utils.colors import Fore
import prettytable


class Output(object):
    @staticmethod
    def print_help(commands):
        s = "     {:12}{}"
        print("     {}     {}".format(Fore.GREEN+"Command"+Fore.END,Fore.GREEN+"Description"+Fore.END))
        print(s.format("-------", "-----------"))
        for item in commands:
            print(s.format(item['name'], item['doc']))

    @staticmethod
    def print_plugin(commands):
        s = "     {:12}{}"
        print("     {}      {}".format(Fore.GREEN + "Plugin" + Fore.END, Fore.GREEN + "Description" + Fore.END))
        print(s.format("-------", "-----------"))
        for item in commands:
            print(s.format(item['name'], item['doc']))

    @staticmethod
    def print_homework(subject):
        print(Fore.GREEN+"[+]"+subject['name']+Fore.END)
        for item in subject['homeworks']:
            print(Fore.MAGENTA+"[-]{:30}{:20}{:20}".format(item['name'],item['start'],item['end'])+Fore.END)

    @staticmethod
    def print_score(subjects):
        #打印成绩
        tb=prettytable.PrettyTable()
        tb.align="l"
        tb.field_names=[Fore.GREEN+'课程'+Fore.END,Fore.GREEN+'学分'+Fore.END,Fore.GREEN+'类别'+Fore.END,Fore.GREEN+'成绩'+Fore.END]
        for item in subjects:
            tb.add_row(item)
        print(tb)

    @staticmethod
    def error(msg):
        print(Fore.RED + "[!]" + msg + Fore.END)

    @staticmethod
    def info(msg):
        print(Fore.GREEN + msg + Fore.END)

    @staticmethod
    def banner():
        s='''
        _________  ________   ____ _____
        \_   ___ \ \_____  \ |    |    /
        /    \  \/  /  / \  \|    |   /
        \     \____/   \_/.  \    |  /
         \______  /\_____\ \_/______/
                \/        \__>
|'============================================'|
||                             sin1ght@qq.com ||
||            https://github.com/taopeach1998 ||
'=============================================='
        '''
        print(s)
