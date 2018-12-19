# pip install elasticsearch
import elasticsearch
from datetime import datetime
from pymongo import MongoClient

print('connecting to db')
# client = MongoClient()
client = MongoClient()
db = client.legal_ai
cases = db.cases

print('connected')
print('starting upload')
date = datetime(1980, 1, 1)
es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200
all_cases = cases.find({ "decision_date":{"$gte":date}})
id=1
for each_case in all_cases:
    new_data = { "id": str(each_case['_id']), "case_body": each_case['case_body'] }
    es.index(index='case_law', doc_type='case_body', id=id, body=new_data)
    id+=1

print('completed... checking for `contract breach` in the dataset')
es.search(index='case_law', q='contract breach')