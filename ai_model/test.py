import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("vigama-ai-hacks-firebase-adminsdk-5waoy-cd77f2333b.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

data = []
data_ref = db.collection('data')
data_docs = data_ref.stream()

for data_doc in data_docs:
    date = data_doc.id

    record_ref = data_ref.document(date).collection('dataType')
    record_docs = record_ref.stream()

    records = []
    for record_doc in record_docs:
        record = {
            'dataType': record_doc.get('dataType'),
            'metric': record_doc.get('metric'),
            'measurement': record_doc.get('measurement')
        }
        records.append(record)

    data_item = {
        'date': date,
        'record': records
    }
    data.append(data_item)