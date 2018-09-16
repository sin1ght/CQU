# CQU
>重大多个系统的命令行客户端,目前可以进入教务网和sakai,对会话进行了缓存，各个系统之间切换非常快速便捷


### 0x1环境
>Pipfile,Pipfile.lock中可以看到所有依赖信息

git clone https://github.com/taopeach1998/CQU.git

pipenv --python 3
 
pipenv install

pipenv shell

python manage.py

### 0x2使用
>当前教务网系统实现查成绩功能，sakai系统实现查看本学期课程未完成作业功能

- help可以查看当前可用命令
- help [命令] 可以查看命令使用方式
- 可以在conf/config.ini 中手动配置账号密码，也可以使用cconfig 命令配置
- jww是教务网账号密码,com_login是统一认证登录账号密码

![](https://upload-images.jianshu.io/upload_images/14069474-325da5a2928d3b1a.gif?imageMogr2/auto-orient/strip)


### 0x3插件
>可以以插件的方式向现有的jww,sakai系统增加新的功能,只需要在plugin/sakai或者plugin/jww中添加文件即可

一个例子

```python
'''
:desc:这是一个测试
:usage:
test
'''


def run(session,args):
    '''
    :param session: requests.Session对象,当前系统的会话
    :param args:一个列表
    '''
    print('this is a test!')
```

- 文件名字就是插件名字
- :desc: 插件描述
- :usage: 插件使用方式
- run函数必须存在
