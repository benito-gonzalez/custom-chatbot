from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms import OpenAI
from scraper.helpers import Topics
import streamlit as st
import openai
import os

my_path = os.path.abspath(os.path.dirname(__file__))
DOCUMENTS_PATH = os.path.join(my_path, "..", "..", "scraper", "documents")
STORAGE_PATH = os.path.join(my_path, "..", "..", 'storage')

os.environ['OPENAI_API_KEY'] = st.secrets["api_crendentials"]
openai.api_key = st.secrets.api_crendentials


def create_directory(topic: str) -> str:
    dir = os.path.join(STORAGE_PATH, topic)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


def generate_indexes():
    for topic in Topics:
        dir = create_directory(topic.value)
        print(f"Starting the document loading for {topic.value}...")
        documents = SimpleDirectoryReader(os.path.join(DOCUMENTS_PATH, topic.value)).load_data()
        llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=256)
        service_context = ServiceContext.from_defaults(llm=llm)

        print("Starting the indexing process...")
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)

        print("storing the index to disk")
        index.storage_context.persist(persist_dir=dir)


@st.cache_resource
def load_indexes(topic):
    storage_context = StorageContext.from_defaults(persist_dir=os.path.join(STORAGE_PATH, topic.value))
    return load_index_from_storage(storage_context)


if __name__ == "__main__":
    generate_indexes()
