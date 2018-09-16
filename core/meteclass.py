import re


class ManagerMetaClass(type):
    def __new__(cls, name, bases, attrs):
        commands=[]
        for k,v in attrs.items():
            if not k.startswith('__') and not k.startswith('_'):
                if v.__doc__ and ':command:' in v.__doc__:
                    doc=re.search(':doc:(.*)',v.__doc__).group(1)
                    commands.append({
                        'name':k,
                        'doc':doc
                    })

        if name!="BaseManager":
            attrs['commands'] = bases[0].commands+commands
        else:
            attrs['commands']=commands

        return type.__new__(cls, name, bases, attrs)
