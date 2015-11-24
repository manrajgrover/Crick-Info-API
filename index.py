from flask import Flask
from flask import jsonify
from bs4 import BeautifulSoup
import urllib
import re
import json
import unicodedata
app = Flask(__name__)

def remove_brackets(text):
    ret = re.sub('\[.+?\]', '', text)
    ret = re.sub('\(.+?\)','', ret)
    return ret

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
        cricketer = cricketer.replace (' ', '_')
        url = 'https://en.wikipedia.org/wiki/'+str(cricketer)
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)
        current = None
        for row in soup.find("table", {"class": "infobox vcard"}).findAll('tr'):
            children = row.find_all(True, recursive=False)
            if len(children) == 1:
                if children[0].name == 'th':
                    current = unicodedata.normalize('NFKD',children[0].text).encode('ascii','ignore')
                    current = current.lower().replace(' ','_').strip()
                    res[current] = {}
                elif children[0].name == 'td' and children[0].table:
                    first = True
                    list = []
                    for r in children[0].table.findAll('tr'):
                        if first:
                            f = True
                            ths = r.find_all(True, recursive=False)
                            for head in ths:
                                if not f:
                                    key = unicodedata.normalize('NFKD', head.text).encode('ascii','ignore')
                                    key = remove_brackets(key).lower().replace('.','').strip().replace(' ','_')
                                    res[current][key] = {}
                                    list.append(key)
                                else:
                                    list.append(key)
                                    f= False
                            first = False
                        else:
                            ths = r.find_all(True, recursive=False)
                            key = unicodedata.normalize('NFKD',ths[0].text).encode('ascii','ignore')
                            key = remove_brackets(key).lower().replace('.','').strip().replace(' ','_')
                            f = True
                            i = 1
                            for head in list:
                                if not f:
                                    value = unicodedata.normalize('NFKD',ths[i].text).encode('ascii','ignore')
                                    value = remove_brackets(value).replace('\n','').strip()
                                    if value.endswith('/'):
                                        value += "0"
                                    i += 1
                                    res[current][head][key] = value 
                                else:
                                    f= False
            elif len(children) == 2:
                if current is not None:
                    value = unicodedata.normalize('NFKD',children[1].text).encode('ascii','ignore')
                    key = unicodedata.normalize('NFKD',children[0].text).encode('ascii','ignore')
                    key = remove_brackets(key).lower().replace('.','').strip().replace(' ','_')
                    value = remove_brackets(value).replace('\n','').strip()
                    res[current][key] = value
        return jsonify(res)

@app.route('/')
@app.route('/index')
def index():
    return 'Welcome to Crick Info API, this is currently under development!'

if __name__ == '__main__':
    app.run()
