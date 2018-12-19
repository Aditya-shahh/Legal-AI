from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import bcrypt
import datetime
import requests
import json
import time
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, CategoriesOptions, SemanticRolesOptions
import elasticsearch
from flask_cors import CORS


def connect():
    connection = MongoClient('localhost', 27017)
    handle = connection["flask_reminders"]
    return handle

app = Flask(__name__)
handle = connect()

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def hello():
        return "Hello World!"


@app.route("/api/search-case", methods=['GET'])
def search_case():
        search_string = request.args.get('search_string')
        es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200
        # es.search(index='case_law', q='contract breach')
        result = es.search(index='case_law', q=search_string)
        search_results = []

        for each_hit in result['hits']['hits']:
                search_results.append({'id':each_hit['_source']['id'], 'case_body':each_hit['_source']['case_body']})
        summarized_search_result = summarize_case(search_results)
        return json.dumps({ 'summarized_search_result' : summarized_search_result })



def summarize_case(search_results):
        summary = ''
        for index,each_result in enumerate(search_results):
                natural_language_understanding = NaturalLanguageUnderstandingV1(version='2018-11-16',iam_apikey='fhfAp9h12U5DSbZ0AzPomZ-suKwnboNAg3EdorPHsB5e',url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api')
                search_results[index]['analytics'] = natural_language_understanding.analyze(text=each_result['case_body'],language='en',features=Features(categories=CategoriesOptions(limit=3),semantic_roles=SemanticRolesOptions())).get_result()
                for role in search_results[index]['analytics']['semantic_roles']:
                        if role['sentence'] not in summary:
                                summary+=' '+role['sentence']
                search_results[index]['analytics']['summary']=summary
                
        return search_results
        # natural_language_understanding = NaturalLanguageUnderstandingV1(version='2018-11-16',iam_apikey='fhfAp9h12U5DSbZ0AzPomZ-suKwnboNAg3EdorPHsB5e',url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api')
        # res = natural_language_understanding.analyze(text='What the hell is going on!!!!',features=Features(categories=CategoriesOptions(limit=3))).get_result()
        # print(res)

if __name__ == "__main__":
        app.run()
