from hashlib import sha1
from hmac import new as hmac
import urllib2
import json
import urllib
import pprint
import sqlite3

'''Simple usage of the signed key API endpoints.'''
publickey = "APIK-K1KBVOlbTDElXVMa86sn5zHnsyF"
privatekey = "RmpGihBgvJx9pT2cYk7Q0RbeFeSKlQ8f"

# Connect to mysql and add our keys
# http://pythoncentral.io/introduction-to-sqlite-in-python/
# db = sqlite3.connect('searchcode.sqlite')
# cursor = db.cursor()
# cursor.execute("DELETE FROM api WHERE publickey = '%s'" % (publickey))
# db.commit()
# cursor.execute('INSERT INTO api (publickey,privatekey,lastused,data) VALUES (?,?,?,?)', (publickey, privatekey, '', ''))
# db.commit()

blns = None
try:
    blns = open('./assets/blns/blns.txt')
except:
    blns = open('../blns/blns.txt')

repotype = "git"
for line in blns:
    reponame = line
    repourl = line
    repousername = line
    repopassword = line
    reposource = line
    repobranch = line

    message = f"pub={urllib.quote_plus(publickey)}&reponame={urllib.quote_plus(reponame)}&repourl={urllib.quote_plus(repourl)}&repotype={urllib.quote_plus(repotype)}&repousername={urllib.quote_plus(repousername)}&repopassword={urllib.quote_plus(repopassword)}&reposource={urllib.quote_plus(reposource)}&repobranch={urllib.quote_plus(repobranch)}"

    sig = hmac(privatekey, message, sha1).hexdigest()

    url = f"http://localhost:8080/api/repo/add/?sig={urllib.quote_plus(sig)}&{message}"

    if len(url) < 2000:
        data = urllib2.urlopen(url)
        assert 200 == data.getcode()

    message = f"pub={urllib.quote_plus(publickey)}&reponame={urllib.quote_plus(reponame)}"

    sig = hmac(privatekey, message, sha1).hexdigest()
    url = f"http://localhost:8080/api/repo/delete/?sig={urllib.quote_plus(sig)}&{message}"

    if len(url) < 2000:
        data = urllib2.urlopen(url)
        assert 200 == data.getcode()

# cursor.execute("DELETE FROM api WHERE publickey = '%s'" % (publickey))
# cursor.execute("DELETE FROM repo")
# db.commit()
