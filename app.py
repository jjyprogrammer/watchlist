from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello	Totoro!</h1><img	src="http://helloflask.com/totoro.gif">'

@app.route('/home')
def hello_home():
    return 'welcome to my watchlist'

@app.route('/user/<name>')
def user_page(name):
    return 'User : %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name = 'jjy'))
    print(url_for('test_url_for', num = 2))
    return 'Test page'


if __name__ == '__main__':
    app.run(debug = True)

