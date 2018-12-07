# coding: utf-8
from flask import Flask, request, make_response, jsonify
from neo4jrestclient.client import GraphDatabase
import sys
import functools

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
url = "http://" + sys.argv[1] + ":" + sys.argv[2] + "@" + sys.argv[3] +":7474/db/data/"
gdb = GraphDatabase(url)

def get_index():
    return "API test page"

def get_hint_top(self, node):
    query = "MATCH (:DBpedia{name:\""+ node +"\"})-[h:hint{rank:\"1\"}]->(to:DBpedia) RETURN h.hint;"
    results = gdb.query(query).get_response()
    return str2json(results)

def get_hint_all(node):
    query = "MATCH (:DBpedia{name:\""+ node +"\"})-[h:hint]->(to:DBpedia) RETURN h;"
    results = gdb.query(query).get_response()
    return str2json(results)

def get_hint_rank(node, rank):
    query = "MATCH (:DBpedia{name:\""+ node +"\"})-[h:hint{rank:\""+str(rank)+"\"}]->(to:DBpedia) RETURN h;"
    results = gdb.query(query).get_response()
    return str2json(results)

def str2json(string):
    results = "{\n"
    results += "\t\"count\":" + str(len(string["data"])) + ",\n"
    results += "\t\"results\":[\n"
    for item in string["data"]:
        for fact in item:
            if len(fact["data"]) != 0:
                results += "\t\t{\n"
                for att in fact["data"].items():
                    k, v = att
                    results += "\t\t\t\""+k+"\":\""+v+"\",\n"
                results = results[:-2]
                results += "\n\t\t},\n"
    results = results[:-2]
    results += "\n\t]\n}"
    return results

def usrpswd(usr, pswd):
    def _usrpswd(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not request.headers.get("username") == usr or not request.headers.get("password") == pswd:
                error_message = {
                    'error': 'username or password is invalid.'
                }
                return make_response(jsonify(error_message), 400)
            return func(*args, **kwargs)
        return wrapper
    return _usrpswd


@app.route('/')
@usrpswd(sys.argv[1], sys.argv[2])
def index():
    return get_index()

@app.route("/api/hint_top/<node>", methods=['GET'])
@usrpswd(sys.argv[1], sys.argv[2])
def hint_top(node):
    return get_hint_top(node)

@app.route("/api/hint_all/<node>", methods=['GET'])
@usrpswd(sys.argv[1], sys.argv[2])
def hint_all(node):
    return get_hint_all(node)

@app.route("/api/hint_rank/<node>&<rank>", methods=['GET'])
@usrpswd(sys.argv[1], sys.argv[2])
def hint_rank(node, rank):
    return get_hint_rank(node, rank)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)



