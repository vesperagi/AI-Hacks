import json
import os
import pip
from pprint import PrettyPrinter as pp
from datetime import datetime
from pathlib import Path
import chatbot
import re

try:
    import pandas as pd
    from google.cloud import firestore
    import urllib.request
    import firebase_admin
    from firebase_admin import credentials, firestore
except:
    pip.main(['install', 'pandas'])
    pip.main(['install', 'firebase_admin'])
    pip.main(['install', 'google-cloud-firestore'])
    import pandas as pd
    from google.cloud import firestore
    import firebase_admin
    from firebase_admin import credentials


def camel_to_snake(camel_case) -> str:
    """
    Convert a string in CamelCase format to snake_case format.

    Parameters
    ----------
    camel_case : str
        String in CamelCase format.

    Returns
    -------
    str
        Converted string in snake_case format.
    """
    split: list = re.findall('[A-Z][^A-Z]*', camel_case)
    first = camel_case[:]
    for camel_back in split:
        first = first.replace(camel_back, "")
    split = list(map(lambda item: item.lower(), split))
    split = list(filter(lambda item: item != '', split))
    after_first = "_".join(split)
    if after_first == '':
        snake_case = first
    else:
        snake_case = first + "_" + after_first
    return snake_case


def camel_to_normal(camel_case) -> str:
    snake = camel_to_snake(camel_case)
    normal = snake.replace("_", " ")
    return normal


def firestore_to_df(credentials: dict = None):
    db = firestore.Client()
    users = list(db.collection(u'users').stream())
    users_dict = list(map(lambda x: x.to_dict(), users))
    df = pd.DataFrame(users_dict)
    return df


def firebase_url_to_df(url: str):
    with urllib.request.urlopen(url) as url_file:
        df = pd.read_csv(url_file)
        return df


def get_firebase_data(debug: bool = False):
    # Specify the path to the JSON file
    file_path = "sandbox/firebase_data.json"

    path = Path(file_path)

    if path.exists():
        print("firebase_data.json exists")

        # Read the JSON file
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return data
    else:
        print("File does not exist")

    print("Connecting to db...")
    cred = credentials.Certificate(
        r"C:\repo\AI-Hacks\ai-architecture\sandbox\vigama-ai-hacks-firebase-adminsdk-5waoy-62752d499a.json")
    firebase_admin.initialize_app(cred)
    # # Get a reference to the Firestore database
    db = firestore.client()

    print("Connected to DB!")

    data = []
    data_ref = db.collection('data')
    data_docs = data_ref.stream()

    print("Getting data...")
    for data_doc in data_docs:
        date = data_doc.id

        record_ref = data_ref.document(date).collection('dataTypes')
        if debug: print(f"DEBUG: record_ref: {record_ref}")
        record_docs = record_ref.stream()
        if debug: print(f"DEBUG: record_docs: {record_docs}")

        records = []
        for record_doc in record_docs:
            if debug: print(f"record_doc: {record_doc}")
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
        if debug: print(f"records: {records}")

    print("Got data!")

    # Open the file in write mode and write the dictionary as JSON
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)
    return data


def data_to_df(data):
    print("Creating DataFrame...")
    df = pd.DataFrame()
    for item in data:
        print("Getting new item")
        date = item["date"]
        records = item["record"]
        for record in records:
            print("\tGetting new record")
            new_row = pd.Series(record, name=date)
            df = df._append(new_row)

    print("Created DataFrame!")
    return df


def data_to_df(data):
    print("Creating DataFrame...")
    df = pd.DataFrame()
    for item in data:
        print("Getting new item")
        date = item["date"]
        records = item["record"]
        for record in records:
            print("\tGetting new record")
            record["date"] = str(date)
            new_row = pd.Series(record)
            df = df._append(new_row, ignore_index=True)

    print("Created DataFrame!")
    return df


def data_to_text_slow(data, file_name="data", debug=False):
    print("Creating textfile...")
    text = ""
    num_entries = len(data)
    for i in range(num_entries):
        if debug: print(f"Parsing item {i} / {num_entries}")
        item = data[i]
        prompt = f"""I will provide you with a JSON of my health data. 
        Please express my data in this JSON using a paragraph.
        
        JSON Data: 
        {item}
        """
        health_summary = chatbot.ai_request(prompt)
        if debug: print("Finished parsing!")
        text += health_summary
        text += "\n\n"

    # # text = "Using an LLM in isolation is fine for simple applications, but more complex applications require chaining LLMs - either with each other or with other components."
    with open(f"{file_name}.txt", 'w', encoding="utf-8") as data_text:
        data_text.write(text)
        data_text.close()
    print("Created textfile!")
    return f"{file_name}.txt"


def data_to_text_fast(data, file_name="data", debug=False):
    print("Creating textfile...")
    text = ""
    num_entries = len(data)
    for i in range(num_entries):
        if debug: print(f"Parsing item {i} / {num_entries}")
        item = data[i]
        date = item["date"]
        records = item["record"]
        text += f"On {date}, the following health measurements were taken: \n"
        for record in records:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%B %d, %Y")
            text += f"On {formatted_date}, data measurements for " \
                    f"{camel_to_normal(record['dataType'])} were " \
                    f"{record['measurement']} {camel_to_normal(record['metric'])}"
            text += "\n"
        text += "\n\n"
        if debug: print("Finished parsing!")

    # # text = "Using an LLM in isolation is fine for simple applications, but more complex applications require chaining LLMs - either with each other or with other components."
    with open(f"{file_name}.txt", 'w', encoding="utf-8") as data_text:
        data_text.write(text)
        data_text.close()
    print("Created textfile!")
    return f"{file_name}.txt"


if __name__ == "__main__":
    print(camel_to_snake("distanceWalkingRunning").replace("_", " "))
    # cred = credentials.Certificate(r"C:\repo\AI-Hacks\ai-architecture\sandbox\vigama-ai-hacks-firebase-adminsdk-5waoy-62752d499a.json")
    # firebase_admin.initialize_app(cred)
    # # # Get a reference to the Firestore database
    # db = firestore.client()
    # #
    # # # Retrieve data from the Firestore database
    # # # # Example: Get a collection named "users"
    # # data_ref = db.collection("data").document("activeEnergyBurned")
    # # docs = data_ref.get()
    # #
    # # # Iterate over the documents in the collection
    # # for doc in docs:
    # #     # Access the data in each document
    # #     data = doc.to_dict()
    # #     # Do something with the data
    # #     print(data)
    #
    # data = []
    # data_ref = db.collection('data')
    # data_docs = data_ref.stream()
    #
    # for data_doc in data_docs:
    #     data_type = data_doc.id
    #     metric = data_doc.get('metric')
    #
    #     record_ref = data_ref.document(data_type).collection('record')
    #     record_docs = record_ref.stream()
    #
    #     records = []
    #     for record_doc in record_docs:
    #         record = {
    #             'date': record_doc.get('date'),
    #             'measurement': record_doc.get('measurement')
    #         }
    #         records.append(record)
    #
    #     data_item = {
    #         'dataType': data_type,
    #         'metric': metric,
    #         'record': records
    #     }
    #     data.append(data_item)
    # pp().pprint(data[0:10])
    data = get_firebase_data()
    text = data_to_df(data)
    print(text)
    # pp().pprint(data)
