# using: utf-8
import requests
import sys

url = 'http://127.0.0.1:8080/api/hint_all/'
node = "欧州連合"
headers = {"username": sys.argv[1], "password": sys.argv[2]}
req = requests.get(url+node, headers=headers)
print(req.text)