from flask import Flask
from flask import jsonify
from bs4 import BeautifulSoup
import urllib
import json
app = Flask(__name__)

@app.route('/api/')
@app.route('/api/<cricketer>')
def api(cricketer=None):
    if cricketer == None:
        res = {}
        res['error'] = True
        res['message'] = 'Please provide a cricketer name as GET parameter'
        return jsonify(res)
    else:
        res = {}
        try:
            cricketer = cricketer.replace (" ", "_")
            url = 'https://en.wikipedia.org/wiki/'+str(cricketer)
            html = urllib.urlopen(url).read()
            soup = BeautifulSoup(html)
            soup = soup.find("table", {"class": "infobox vcard"})
        except:
            return flask.response()
        return jsonify(res)

@app.route('/')
@app.route('/index')
def index():
    return 'Welcome to Crick Info API, this is currently under development!'

if __name__ == '__main__':
    app.run()
