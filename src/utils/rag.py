from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms import OpenAI, Replicate
from scraper.helpers import Topics, Models
import streamlit as st
import openai
import os

my_path = os.path.abspath(os.path.dirname(__file__))
DOCUMENTS_PATH = os.path.join(my_path, "..", "..", "scraper", "documents")
STORAGE_PATH = os.path.join(my_path, "..", "..", 'storage')

os.environ['OPENAI_API_KEY'] = st.secrets["api_crendentials"]
openai.api_key = st.secrets.api_crendentials


def create_directory(model: str, topic: str) -> str:
    dir = os.path.join(STORAGE_PATH, model, topic)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


def generate_indexes():
    model_params = {
        Models.GPT: {"model": "gpt-3.5-turbo", "temperature": 0, "max_tokens": 256},
        Models.LLAMA2: {"model": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3"}
    }

    for model in Models:
        for topic in Topics:
            dir = create_directory(model.value, topic.value)
            print(f"Starting the document loading for {topic.value} in {model.value}...")
            documents = SimpleDirectoryReader(os.path.join(DOCUMENTS_PATH, topic.value)).load_data()

            model_params_current = model_params.get(model, {})
            llm = OpenAI(**model_params_current) if model == Models.GPT else Replicate(**model_params_current)

            service_context = ServiceContext.from_defaults(llm=llm)

            print("Starting the indexing process...")
            index = VectorStoreIndex.from_documents(documents, service_context=service_context)

            print("storing the index to disk")
            index.storage_context.persist(persist_dir=dir)


@st.cache_resource
def load_indexes(model, topic):
    storage_context = StorageContext.from_defaults(persist_dir=os.path.join(STORAGE_PATH, model.value, topic.value))
    return load_index_from_storage(storage_context)


if __name__ == "__main__":
    generate_indexes()
