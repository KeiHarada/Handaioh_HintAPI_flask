# coding: utf-8
from flask import Flask, request, make_response, jsonify
from neo4jrestclient.client import GraphDatabase
import sys
import functools
from flask_cors import CORS
from pprint import pprint

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False
url = "http://" + sys.argv[1] + ":" + sys.argv[2] + "@" + sys.argv[3] +":7474/db/data/"
gdb = GraphDatabase(url)

def get_index():
    return "API test page"

def get_hint_top(node):
    query = "MATCH (:DBpedia{dbpedia:\""+ node +"\"})-[h:hint{rank:\"1\"}]->(:DBpedia) RETURN h;"
    results = gdb.query(query).get_response()

    return str2json(results, node)

def get_hint_all(node):
    query = "MATCH (:DBpedia{dbpedia:\""+ node +"\"})-[h:hint]->(:DBpedia) RETURN h;"
    results = gdb.query(query).get_response()
    return str2json(results, node)

def get_hint_rank(node, rank):
    query = "MATCH (:DBpedia{dbpedia:\""+ node +"\"})-[h:hint]->(:DBpedia) WHERE h.rank<=\""+str(rank)+"\" RETURN h;"
    results = gdb.query(query).get_response()
    return str2json(results, node)

def str2json(string, node):

    results = dict()
    results["seikai"] = node
    results["count"] = str(len(string["data"]))
    results["results"] = list()
    for item in string["data"]:
        for fact in item:
            results["results"].append(fact["data"])
    results = jsonify(results)
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
#@usrpswd(sys.argv[1], sys.argv[2])
def index():
    return get_index()

@app.route("/api/hint_top/<node>", methods=['GET'])
#@usrpswd(sys.argv[1], sys.argv[2])
def hint_top(node):
    return get_hint_top(node)

@app.route("/api/hint_all/<node>", methods=['GET'])
#@usrpswd(sys.argv[1], sys.argv[2])
def hint_all(node):
    return get_hint_all(node)

@app.route("/api/hint_rank/<node>&<rank>", methods=['GET'])
#@usrpswd(sys.argv[1], sys.argv[2])
def hint_rank(node, rank):
    return get_hint_rank(node, rank)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)



