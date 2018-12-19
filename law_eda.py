# pip install pymongo
# pip install jsonlines

import jsonlines
from pymongo import MongoClient
import xml.etree.ElementTree as ET
import datetime

client = MongoClient()
db = client.legal_ai
cases = db.cases

print("about to upload jsonl file to local mongodb")
id_saved = []
with jsonlines.open('./data.jsonl') as reader:
    for obj in reader:
        if int(obj['decision_date'][0:4])>1950:
            case_id = cases.insert_one(obj).inserted_id
            id_saved.append(case_id)

print("Added all the files... No of documents added: "+str(len(id_saved)))

all_cases = cases.find()

for each_case in all_cases:

    # String to timestamp format
    try:
        decision_date = datetime.datetime.strptime(each_case['decision_date'], "%Y-%m-%d %H:%M:%S")
    except:
        try:
            decision_date = datetime.datetime.strptime(each_case['decision_date'], "%Y-%m-%d")
        except:
            try:
                decision_date = datetime.datetime.strptime(each_case['decision_date'], "%Y-%m")
            except:
                try:
                    decision_date = datetime.datetime.strptime(each_case['decision_date'], "%Y")
                except:
                    pass

    # clean xml dataset to pure string for nlp
    root = ET.fromstring(each_case['casebody']['data'])
    summary=''
    for child in root:
        for sub_child in child:
            if 'footnotemark' in sub_child.tag[sub_child.tag.index("}")+1:] or 'author' in sub_child.tag[sub_child.tag.index("}")+1:]:
                continue
            summary+=sub_child.text + "\n"
    
    # Update each case
    myquery = { "_id": each_case['_id'] }
    newvalues = { "$set": { "case_body": summary, "decision_date": decision_date } }
    cases.update_one(myquery, newvalues)

print('completed. Check database');