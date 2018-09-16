import os


APP_DIR=os.path.join(os.path.abspath(os.path.dirname(__file__)),'../')
PLUGIN_DIR=os.path.join(APP_DIR,'plugin')


if __name__ == '__main__':
    print(os.path.isfile(os.path.join(APP_DIR,'Pipfile')))