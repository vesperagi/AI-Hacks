import pip
from utils import get_firebase_data, data_to_text_fast
from langchain import HuggingFaceHub
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
    # pip install "jax[cpu]===0.3.14" -f https://whls.blob.core.windows.net/unstable/index.html --use-deprecated legacy-resolver
    pip.main(['install', 'wrapt'])
    pip.main(['install', 'torch'])
    pip.main(['install', 'tensorflow'])
    pip.main(['install', 'flax'])
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

try:
    from transformers import AutoModel, AutoTokenizer, AutoConfig
except:
    pip.main(["install", "transformers"])
    from transformers import AutoModel, AutoTokenizer, AutoConfig

pinecone.init(
    api_key="7c732676-2e8f-4b8a-aeb8-3c022ea21118",
    environment="asia-southeast1-gcp-free",
)


tokinizer= AutoTokenizer.from_pretrained('UFNLP/gatortron-medium')
config=AutoConfig.from_pretrained('UFNLP/gatortron-medium')
mymodel=AutoModel.from_pretrained('UFNLP/gatortron-medium')

encoded_input=tokinizer("Bone scan:  Negative for distant metastasis.", return_tensors="pt")
encoded_output = mymodel(**encoded_input)

data = get_firebase_data()
text = data_to_text_fast(data)


def determine_health_use(input: str) -> str:
    prompt: str = f"""Determine if the following question warrants use of the health database where it stores all the health related data collected, or the conversation log data base where it stores all the previous conversation. REturn True if it is health database, and False if it is convo log database.

    example question: can you give me my average heart rate over the past week?
    true

    question: {input}
    """
    response = ai_request(prompt, system_role="You are a health guidance figure helping a user live a healthy life.")
    health_use = response.lower().replace(".", "")
    return health_use

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

    repo_id = "UFNLP/gatortron-medium"  # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options

    qa = VectorDBQA.from_chain_type(
        llm=HuggingFaceHub(repo_id=repo_id,
                           model_kwargs={"temperature": 0.8,
                                         "max_length": 64}),
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
        try:
            response = chatbot_response(query)
        except:
            response = ai_request(query)
        pprint.PrettyPrinter().pprint(response)
