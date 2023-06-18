import os
import time

import pip
from src.llms.chatbot import ai_request
import json
from pathlib import Path
import numpy as np
from datetime import datetime

try:
    from langchain.document_loaders import TextLoader, JSONLoader, DataFrameLoader
    from langchain.text_splitter import CharacterTextSplitter
    import langchain
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.vectorstores import Pinecone
    from langchain import VectorDBQA, OpenAI
    import pinecone
    from flask import Flask, request, jsonify
    import pandas as pd
    from google.cloud import firestore
    import urllib.request
    import firebase_admin
    from firebase_admin import credentials, firestore
except:
    pip.main(['install', 'langchain'])
    pip.main(['install', 'flask'])
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
    from flask import Flask, request, jsonify
    import firebase_admin
    from firebase_admin import credentials
    from langchain.document_loaders import TextLoader
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.vectorstores import Pinecone
    from langchain import VectorDBQA, OpenAI
    import pinecone
    from pinecone import PineconeClient

pinecone.init(
    api_key="7c732676-2e8f-4b8a-aeb8-3c022ea21118",
    environment="asia-southeast1-gcp-free",
)

pinecone_client = PineconeClient(api_key="7c732676-2e8f-4b8a-aeb8-3c022ea21118")

app = Flask(__name__)


def get_firebase_data(debug: bool = False):
    """
    This function will firstly check if the file 'firebase_data.json' exists in the current directory. If found, it will read and return the data from the JSON file.

    If the file is not found, the function will attempt to connect to the Firebase Firestore database and pull data from a 'data' collection there.

    For each document in the 'data' collection, a record is created with fields 'dataType', 'metric' and 'measurement' and added to a list of records. This list, together with the document's id (date), forms an data item.

    All data items are added to a collection, which is turned into a JSON object and saved as 'firebase_data.json' in the current directory.

    Parameters
    ---------
    debug : bool, optional
        If true, additional debug information will be printed to the console.

    Returns
    -------
    list
        List of dictionaries containing the data collected from the 'data' collection in the Firestore database or
        from the 'firebase_data.json' file if it exists in the current directory.
    """
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


def get_music_data(debug: bool = False):
    """
    Fetches music data from Firestore database or from a local JSON file if it exists.

    Parameters
    ---------
    debug : bool, optional
        A flag to toggle the debug mode. Default is set to False.

    Returns
    -------
    list
        List of music data as dictionaries. Each dictionary can contain three keys: 'date', 'sentiment' and 'title'.
    """
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
    data_ref = db.collection('music')
    data_docs = data_ref.stream()

    for data_doc in data_docs:
        data_item = {
            'date': data_doc.get('date'),
            'sentiment': data_doc.get('sentiment'),
            'title': data_doc.get('title')
        }
        data.append(data_item)

    # Open the file in write mode and write the dictionary as JSON
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)
    return data


def data_to_df(data):
    """
    Creates a DataFrame from a collection of dictionaries.

    Parameters
    ---------
    data : list
        List of dictionaries with key-value pairs, each key represents a column in the DataFrame and the values represent the data entries per column.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame created from the input data.

    Side Effects
    ------------
    Prints "Creating DataFrame..." at the beginning of the function.
    Prints "Getting new item" before iterating over records within a dictionary item.
    Prints "Getting new record" before appending each new record into the DataFrame.
    Prints "Created DataFrame!" at the end of the function.
    """
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
    """
    Provide decision on which database to use based on the input question.

    This function helps in determining whether to use the health database storing all health related data or the conversation log
    database storing all previous conversations. Returns True if health database is suggested, otherwise False.

    Parameters
    ---------
    input : str
        User input question.

    Returns
    -------
    str
        Returns 'true' if health database is required or 'false' if conversation log database is required.
    """
    prompt: str = f"""Determine if the following question warrants use of the health database where it stores all the health related data collected, or the conversation log data base where it stores all the previous conversation. REturn True if it is health database, and False if it is convo log database.

    example question: can you give me my average heart rate over the past week?
    true

    question: {input}
    """
    response = ai_request(prompt, system_role="You are a health guidance figure helping a user live a healthy life.")
    health_use = response.lower().replace(".", "")
    return health_use


def fetch_last_vector():
    """
    Fetches the last vector from Pinecone's index.

    This function connects to the Pinecone client and fetches the ids of all the vectors in the given index.
    If there are vectors in the index, it fetches the content of the last vector based on the last id. If the index is
    empty, it returns None.

    Returns
    -------
    dict or None
        Dictionary containing the vector data if it exists, None otherwise.
    """
    vector_ids = pinecone_client.list_index_vectors(index_name=PINECONE_INDEX_NAME)
    if vector_ids:
        last_vector_id = vector_ids[-1]
        last_vector = pinecone_client.fetch_vectors(index_name=PINECONE_INDEX_NAME, ids=[last_vector_id])
        return last_vector[0]
    else:
        return None


def evaluate_vector(vector):
    """
    Evaluates if the magnitude of a given vector is greater than the predetermined threshold.

    Parameters
    ----------
    vector : ndarray
        An input vector that will be evaluated.

    Returns
    -------
    bool
        Returns True if the vector's magnitude is greater than the threshold, False otherwise.
    """
    threshold = 10.0
    magnitude = np.linalg.norm(vector)
    return magnitude > threshold


def health_metrics_monitoring():
    """
    Continuously monitor the health metrics by fetching the last vector every minute.

    If the new vector is different from the last one, evaluate the new vector. Simultaneously, update the last vector to the new one. If the new vector evaluates to True (i.e., abnormal data is detected), it prints a message indicating the time at which the abnormal data was detected.

    The function fetches and evaluates the new vector until the function is stopped.

    Parameters
    ---------
    None

    Returns (prints)
    ---------
    str
        A message indicating the time at which abnormal data was detected if an abnormal vector is detected.

    Note:
    This function runs in a continuous loop and needs to be manually stopped. It fetches a new vector every minute.
    """
    last_vector = None
    while True:
        new_vector = fetch_last_vector()
        if new_vector is not None and new_vector != last_vector:
            # Evaluate the new vector
            if evaluate_vector(new_vector):
                print(f"Abnormal data detected at {datetime.now()}!")
            last_vector = new_vector
        time.sleep(60)


def chatbot_response(user_input: str, debug=False):
    """
    Generate response to user input using pre-trained AI model, tokenizer, and search engine.

    Parameters
    ----------
    user_input : str
        User query to be analyzed.

    debug : Boolean, optional
        Flag indicating if debug logs should be printed.

    Returns
    -------
    result : str
        The generated response to the user query.

    This function reads data from a text file and transforms it into a format suitable for the AI model.
    It then splits up the data into digestible chunks, and retrieves word embeddings using an OpenAI API key.
    These embeddings are then loaded into the Pinecone search engine.

    The function then sets up a Question Answering system by using a pre-trained OpenAI model, and applies the search engine with the document data.
    Finally, the function queries the QA system with the user input and returns the QA system's response.
    """
    text_file_path = os.path.join("test_data.txt")

    loader = TextLoader(
        text_file_path,
        encoding="utf-8"
    )

    document = loader.load()

    # Splitting up documents
    if debug: print("Splitting up documents...")
    text_splitter = CharacterTextSplitter(chunk_size=3000, chunk_overlap=0)

    if debug: print(f"document: {document}")

    texts = text_splitter.split_documents(document)
    if debug: print("Split up documents!")
    if debug: print(f"DEBUG: texts is: {texts}")

    # Pinecone setup for DFs
    if debug: print("Getting OpenAI embeddings...")
    embeddings = OpenAIEmbeddings(openai_api_key="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")
    if debug: print("Got OpenAI embeddings...")

    try:
        if debug: print(f"page_content: {dict(list(texts)[0])['page_content']}")
        if debug: print(f"type(page_content): {type(dict(list(texts)[0])['page_content'])}")
    except:
        pass

    if debug: print("Setting up Pinecone...")
    docsearch = Pinecone.from_documents(
        texts, embeddings, index_name="ai-hack"
    )

    if debug: print("Pinecone setup!")

    if debug: print("Loading Vector Storage into Database Question Answer Chain...")

    qa = VectorDBQA.from_chain_type(
        llm=OpenAI(openai_api_key="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",
                   model_name="gpt-3.5-turbo"),
        chain_type="stuff",
        vectorstore=docsearch,
        return_source_documents=True
    )
    if debug: print("Loaded Answer Chain...")

    if debug: print("Sending user input to langchain...")
    result = qa({"query": user_input})
    result = result["result"]
    if debug: print("Result received from LLM!")
    return result


@app.route('/')
def home():
    """
    Defines a web route that returns a friendly greeting when accessed.

    Parameters
    ---------
    This function does not have any explicit parameters.

    Returns
    -------
    str
        The string 'Hello, world!'
    """
    return 'Hello, world!'


@app.route('/api/chat_input', methods=["POST"])
def post_input():
    """
    Handle POST requests to the /api/chat_input route.

    Parameters
    ---------
    data : dict
        The request body is expected to contain a dictionary with a single key "input". The corresponding value should be a string containing the text to process.

    Returns
    -------
    dict
        Return a dictionary with a single key "response". The corresponding value is the automated response based on the provided input text. The response is returned in string format.

    Notes
    -------
    data is in the form
    {
        "input" : "text"
    }
    """

    # Get the JSON data from the request body
    input = request.form["input"]
    # try:
    result = chatbot_response(input)
    # except:
    # result = ai_request(input)
    return json.dumps({"response": result})


app.run(debug=True)
