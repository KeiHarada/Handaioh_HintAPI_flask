# using: utf-8
import requests
import urllib.parse
import sys

url = 'http://bd-ensyu.ist.osaka-u.ac.jp:15000/api/hint_all/'
node = urllib.parse.unquote("ミヤコシ")
#headers = {"username": sys.argv[1], "password": sys.argv[2]}
req = requests.get(url+node)
print(req.text)