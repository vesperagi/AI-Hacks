import os
import pip
import pprint
from chatbot import ai_request
import json

try:
    from langchain.document_loaders import TextLoader, JSONLoader, DataFrameLoader
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.vectorstores import Pinecone
    from langchain import VectorDBQA, OpenAI
    from utils import firebase_url_to_df
    import pinecone
except:
    pip.main(['install', 'langchain'])
    pip.main(['install', 'pinecone-client'])
    pip.main(['install', 'wheel'])
    pip.main(['install', 'jq'])
    pip.main(['install', 'black'])
    pip.main(['install', 'openai'])
    pip.main(['install', 'tiktoken'])
    from langchain.document_loaders import TextLoader
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.vectorstores import Pinecone
    from langchain import VectorDBQA, OpenAI
    import pinecone

pinecone.init(
    api_key=os.getenv("PINECONE-API-KEY"),
    environment="asia-southeast1-gcp-free",
)


def determine_health_use(input: str) -> str:
    prompt: str = f"""Determine if the following question warrants use of the health database where it stores all the health related data collected, or the conversation log data base where it stores all the previous conversation. REturn True if it is health database, and False if it is convo log database.
    
    example question: can you give me my average heart rate over the past week?
    true
    
    question: {input}
    """
    response = ai_request(prompt)
    health_use = response.lower().replace(".", "")
    return health_use


def chatbot_response(user_input: str) -> str:
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
    loader = DataFrameLoader(
        data_frame=firebase_url_to_df(firebase_url)  # pandas df
    )
    document = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(len(texts))

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI-API-KEY"))
    docsearch = Pinecone.from_documents(
        texts, embeddings, index_name="ai-hack"
    )

    qa = VectorDBQA.from_chain_type(
        llm=OpenAI(openai_api_key=os.getenv("OPENAI-API-KEY")),
        chain_type="stuff",
        vectorstore=docsearch,
        return_source_documents=True
    )
    result = qa({"query": user_input})
    answer = result["result"]
    return answer


if __name__ == "__main__":
    print("DEBUG: Start Chatbot")
    while True:
        query: str = input("User: ")
        response: str = chatbot_response(query)
        pprint.PrettyPrinter().pprint(response)
