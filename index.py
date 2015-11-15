from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index():
    return 'Welcome to Crick Info API, this is currently under development!'

if __name__ == '__main__':
    app.run()
