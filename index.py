from flask import Flask
from bs4 import BeautifulSoup
import urllib
import json
app = Flask(__name__)

@app.route('/api/<cricketer>',methods=['GET'])
def api(cricketer=None):
    res = {}
    if cricketer == None:
        res['error'] = True
        res['message'] = 'Please provide a cricketer name as GET parameter'
        res = json.dumps(res)
    else:
        cricketer = cricketer.replace (" ", "_")
        url = 'https://en.wikipedia.org/wiki/'+str(cricketer)
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)
        soup = soup.find("table", {"class": "infobox vcard"})
    return res

@app.route('/')
@app.route('/index')
def index():
    return 'Welcome to Crick Info API, this is currently under development!'

if __name__ == '__main__':
    app.run()
