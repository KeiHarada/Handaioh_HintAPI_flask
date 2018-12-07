# using: utf-8
import requests

url = 'http://127.0.0.1:15000/'
node = "コンピュータゲーム"
headers = {"username": "neo4j", "password": "hana1oh"}
req = requests.get(url, headers=headers)
print(req.text)