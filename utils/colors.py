class Fore(object):
    _basic="\033[1;{}m"
    BLACK=_basic.format(30)
    RED=_basic.format(31)
    GREEN=_basic.format(32)
    YELLOW=_basic.format(33)
    BLUE=_basic.format(34)
    MAGENTA=_basic.format(35) #洋红
    CYAN=_basic.format(36) #青色
    WHITE=_basic.format(37)
    END="\033[0m"