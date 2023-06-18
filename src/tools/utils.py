import json
import pip
from datetime import datetime
from pathlib import Path
from src.llms import chatbot
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
    """
    Transforms a string from camelCase format into normal format (with spaces instead of underscores).

    Parameters
    ---------
    camel_case : str
        Input string in camelCase format.

    Returns
    -------
    str
        String in normal format.
    """
    snake = camel_to_snake(camel_case)
    normal = snake.replace("_", " ")
    return normal


def firestore_to_df(credentials: dict = None):
    """
    Transforms Firestore data collection into a pandas DataFrame.

    Parameters
    ---------
    credentials : dict, default is None
        Dictionary containing the user credentials.

    Returns
    -------
    DataFrame
        DataFrame containing users data.
    """
    db = firestore.Client()
    users = list(db.collection(u'users').stream())
    users_dict = list(map(lambda x: x.to_dict(), users))
    df = pd.DataFrame(users_dict)
    return df


def firebase_url_to_df(url: str):
    """
    Converts a firebase URL to a pandas DataFrame by reading the content of the URL as CSV.

    Parameters
    ---------
    url : str
        URL string that points to a CSV resource.

    Returns
    -------
    DataFrame
        DataFrame containing the data from the read CSV.
    """
    with urllib.request.urlopen(url) as url_file:
        df = pd.read_csv(url_file)
        return df


def get_firebase_data(debug: bool = False):
    """
    This function retrieves data from Firebase, if Firebase data is not existing in ai-architecture/sandbox/firebase_data.json path then connect to Firebase and get data from Firestore data collection.

    Parameters
    ---------
    debug : bool, optional
        If set to True, the function will output detailed status messages during execution.

    Returns
    -------
    list
        A list of dictionaries, each containing 'date' key with date and 'record' key with data records from Firebase.
    """
    # Specify the path to the JSON file
    file_path = "ai-architecture/sandbox/firebase_data.json"

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
    """
    Create a Pandas DataFrame from the given data.

    Parameters
    ----------
    data : list
        A list of dictionaries where each dictionary has a 'date' key and a 'record' key which
        is a dictionary in itself comprising of record details corresponding to the date.

    Returns
    -------
    DataFrame
        A dataframe where each row represents the record details for a particular date.

    """
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
    """
    Transform a list of records into a Pandas DataFrame, each record is a dictionary object containing date and record data.

    Parameters
    ---------
    data : list
        The list contains the records data where each item is a dictionary object consisting of a date and a record.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the record data. Note that the original date and records within the input list is converted into string format.
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


def data_to_text_slow(data, file_name="data", debug=False):
    """
    Convert a list of JSON data into a textual summary and write the content into a text file.

    Parameters
    ---------
    data : list of dict
        List containing JSON formatted data elements.

    file_name : str
        Name of the file where the converted text data is stored. Default name is 'data'.

    debug : boolean
        If set to True, prints out debug information like parsing progress and completion for each item. Default is False.

    Returns
    -------
    str
        String representing the path to the created text file.
    """
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
    """
    This function converts data containing health information into a readable text file.

    Parameters
    ----------
    data : list of dict
        List of dictionaries containing the date and health record information.
    file_name : str, optional
        The name of the text file to be created (default is "data").
    debug : bool, optional
        If True, print debug statements (default is False).

    Returns
    -------
    str
        The name of the created text file.

    Side Effect
    ------------
    Writes a text file to the local directory.

    """
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


