import os

import openai
import pip
import pprint
from chatbot import ai_request
import json
from pathlib import Path
from pprint import PrettyPrinter as pp
from mapmaker import NestedMap
import numpy as np
from utils import firebase_url_to_df, data_to_text_slow, data_to_text_fast
import firebase
import firebase_admin

try:
    from langchain.document_loaders import TextLoader, JSONLoader, DataFrameLoader
    from langchain.text_splitter import CharacterTextSplitter
    import langchain
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.vectorstores import Pinecone
    from langchain import VectorDBQA, OpenAI
    import pinecone
    import pandas as pd
    from google.cloud import firestore
    import urllib.request
    import firebase_admin
    from firebase_admin import credentials, firestore
except:
    pip.main(['install', 'langchain'])
    pip.main(['install', 'pinecone-client'])
    pip.main(['install', 'wheel'])
    pip.main(['install', 'jq'])
    pip.main(['install', 'black'])
    pip.main(['install', 'openai'])
    pip.main(['install', 'tiktoken'])
    pip.main(['install', 'pandas'])
    pip.main(['install', 'firebase_admin'])
    pip.main(['install', 'google-cloud-firestore'])
    import pandas as pd
    from google.cloud import firestore
    import firebase_admin
    from firebase_admin import credentials
    from langchain.document_loaders import TextLoader
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.vectorstores import Pinecone
    from langchain import VectorDBQA, OpenAI
    import pinecone

pinecone.init(
    api_key="7c732676-2e8f-4b8a-aeb8-3c022ea21118",
    environment="asia-southeast1-gcp-free",
)


def get_firebase_data(debug: bool = False):
    # Specify the path to the JSON file
    file_path = "firebase_data.json"

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
            record["date"] = str(date)
            new_row = pd.Series(record)
            df = df._append(new_row, ignore_index=True)

    print("Created DataFrame!")
    return df


def determine_health_use(input: str) -> str:
    prompt: str = f"""Determine if the following question warrants use of the health database where it stores all the health related data collected, or the conversation log data base where it stores all the previous conversation. REturn True if it is health database, and False if it is convo log database.
    
    example question: can you give me my average heart rate over the past week?
    true
    
    question: {input}
    """
    response = ai_request(prompt, system_role="You are a health guidance figure helping a user live a healthy life.")
    health_use = response.lower().replace(".", "")
    return health_use


# def format_data(data):
#

# ==================================================================
# STAGE 3 IMPLEMENTATION

def health_metrics_monitoring(data):
    # insert health monitoring rules
    # if rule triggers, call GPT
    index = pinecone.Index('openai')

    res = openai.Embedding.create(
        input=[today_data],
        engine="gpt-4"
    )

    today_vector = [record['embedding'] for record in res['data']][0]

    results = index.query(queries=[today_vector], top_k=5)

    avg_distance = np.mean([match['score'] for match in results['results'][0]['matches']])

    if avg_distance > threshold:
        raise_alert()

    index.upsert(ids=[today_date], vectors=[today_vector])

    pass


# ==================================================================

def chatbot_response(user_input: str):
    use_health_db: str = determine_health_use(user_input)
    if use_health_db == "true":
        firebase_url = ...  # health db url
    else:
        firebase_url = ...  # chat db url

    # loader = TextLoader(
    #     r"C:\repo\AI-Hacks\ai-architecture\sandbox\textfiles\blog.txt",
    #     encoding="utf-8"
    # )
    # loader = JSONLoader(
    #     r"C:\repo\AI-Hacks\ai-architecture\sandbox\textfiles\blog.json",
    #     jq_schema='.text'
    # )
    # loader = DataFrameLoader(
    #     data_frame=firebase_url_to_df(firebase_url)  # pandas df
    # )

    # data = get_firebase_data()

    # print(data)

    # text_file_path = data_to_text_fast(data)
    text_file_path = os.path.join("textfiles", "test_data.txt")

    loader = TextLoader(
        text_file_path,
        encoding="utf-8"
    )
    #
    # data = get_firebase_data()
    # loader = DataFrameLoader(
    #     data_frame=data_to_df(data),
    #     page_content_column="date"
    # )

    document = loader.load()

    # # Print the data.
    # for doc in loader.documents:
    #     print(doc)

    # # Pinecone setup for text files
    # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # texts = text_splitter.split_documents(document)
    # print(len(texts))
    # print(f"texts: {texts}")
    #
    # embeddings = OpenAIEmbeddings(openai_api_key="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")
    # docsearch = Pinecone.from_documents(
    #     texts, embeddings, index_name="ai-hack"
    # )

    # Splitting up documents
    print("Splitting up documents...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    print(f"document: {document}")

    texts = text_splitter.split_documents(document)
    print("Split up documents!")
    print(f"DEBUG: texts is: {texts}")

    # Pinecone setup for DFs
    print("Getting OpenAI embeddings...")
    embeddings = OpenAIEmbeddings(openai_api_key="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")
    print("Got OpenAI embeddings...")

    try:
        print(f"page_content: {dict(list(texts)[0])['page_content']}")
        print(f"type(page_content): {type(dict(list(texts)[0])['page_content'])}")
    except:
        pass

    print("Setting up Pinecone...")
    docsearch = Pinecone.from_documents(
        texts, embeddings, index_name="ai-hack"
    )

    with open("docsearch.txt", "w") as docsearch_file:
        try:
            json.dump(docsearch, docsearch_file)
        except:
            print(f"Couldn't save docsearch")
            print(f"Docsearch: {docsearch}")

    print("Pinecone setup!")

    print("Loading Vector Storage into Database Question Answer Chain...")

    qa = VectorDBQA.from_chain_type(
        llm=OpenAI(openai_api_key="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",
                   model_name="gpt-3.5-turbo"),
        chain_type="stuff",
        vectorstore=docsearch,
        return_source_documents=True
    )
    print("Loaded Answer Chain...")

    NestedMap(json.loads(qa.json())).show()

    print("Sending user input to langchain...")
    result = qa({"query": user_input})
    # result = result["result"]
    print("Result received from LLM!")
    return result


if __name__ == "__main__":
    print("DEBUG: Start Chatbot")
    while True:
        query: str = input("User: ")
        response = chatbot_response(query)
        pprint.PrettyPrinter().pprint(response)
