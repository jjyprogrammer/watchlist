import os
from flask import Flask

def test():
    print('1')
    print('2')
    print('3')
    print('4')



    print('6')


print("+++++")
if __name__ == '__main__':
    app = Flask(__name__)
    print('==========')
    print(app.root_path)
    print(os.path)
    print(os.path.join(app.root_path, 'data.db'))
    test()