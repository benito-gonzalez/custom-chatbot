from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms import OpenAI

import streamlit as st
import openai
import os

my_path = os.path.abspath(os.path.dirname(__file__))
DOCUMENTS_PATH = os.path.join(my_path, "..", "..", "scraper", "documents")
INDEXES_PATH = os.path.join(DOCUMENTS_PATH, "indexes")

os.environ['OPENAI_API_KEY'] = st.secrets.api_crendentials
openai.api_key = st.secrets.api_crendentials


def init_rag():
    print("Starting the document loading...")
    documents = SimpleDirectoryReader(DOCUMENTS_PATH).load_data()
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=256)
    service_context = ServiceContext.from_defaults(llm=llm)

    print("Starting the indexing process...")
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)

    print("storing the index to disk")
    index.storage_context.persist(persist_dir=os.path.join(DOCUMENTS_PATH, "indexes"))

    return index


def load_indexes():
    storage_context = StorageContext.from_defaults(persist_dir=INDEXES_PATH)
    return load_index_from_storage(storage_context)
