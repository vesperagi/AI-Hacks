from src.tools.utils import get_firebase_data, data_to_text_fast
from langchain import HuggingFaceHub
import os

import pip
import pprint
from src.llms.chatbot import ai_request
import json
from src.tools.mapmaker import NestedMap

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

def chatbot_response(user_input: str):
    """
    Generates and returns an AI Chatbot's response to the user's input.

    Parameters
    ---------
    user_input : str
        Users' text input for the Chatbot.

    Returns
    -------
    str
        AI Chatbot's text response to the users input.

    Other Attributes
    -----------------
    This function also generates, deploys and saves AI embeddings, Vector search storage, trains a Question-Answer model from Huggingface
    and implements Deep Learning to generate responses to user input.
    """
    # text_file_path = data_to_text_fast(data)
    text_file_path = os.path.join("textfiles", "ai-architecture/test_data.txt")

    loader = TextLoader(
        text_file_path,
        encoding="utf-8"
    )

    document = loader.load()

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
    raw = qa({"query": user_input})
    result = raw["result"]
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
