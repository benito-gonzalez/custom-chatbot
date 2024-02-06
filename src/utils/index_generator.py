import logging
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
    set_global_service_context
)
from typing import List
from llama_index.schema import Document
from scraper.helpers import Topics
from src.utils.models import EmbeddingModelManager, TextModelManager
import streamlit as st
import openai
import os
import shutil

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.INFO)

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


def get_service_context():
    embedding_model = EmbeddingModelManager.get_embedding_model()
    llm = TextModelManager.get_llm()
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embedding_model)
    set_global_service_context(service_context)

    return service_context


def check_empty_dir(path):
    if not os.path.exists(path):
        return 0
    return len(os.listdir(path)) == 0


def move_processed_documents(documents: List[Document], topic: Topics) -> None:
    dir = os.path.join(DOCUMENTS_PATH, topic.value, "processed")
    logging.info(f"Moving the processed documents to {dir}")

    if not os.path.exists(dir):
        os.makedirs(dir)

    for document in documents:
        logging.debug(f"Moving {document.metadata.get('file_name')} to {dir}")
        filepath = document.metadata.get('file_path')
        shutil.move(filepath, dir)


def generate_indexes():
    for topic in Topics:
        logging.info(f"Starting the document loading for {topic.value.capitalize()}...")
        pending_dir = os.path.join(DOCUMENTS_PATH, topic.value, "pending")

        if check_empty_dir(pending_dir):
            logging.info(f"There is no new documents for {topic.value.capitalize()}")
        else:
            documents = SimpleDirectoryReader(pending_dir).load_data()
            service_context = get_service_context()

            logging.info("Starting the indexing process...")
            index = VectorStoreIndex.from_documents(documents, service_context=service_context)

            logging.info("storing the index to disk")
            dir = create_directory(topic.value)
            index.storage_context.persist(persist_dir=dir)

            # move documents to processed directory
            move_processed_documents(documents, topic)


@st.cache_resource
def load_indexes(topic):
    storage_context = StorageContext.from_defaults(persist_dir=os.path.join(STORAGE_PATH, topic.value))
    service_context = get_service_context()
    return load_index_from_storage(storage_context, service_context=service_context)


if __name__ == "__main__":
    generate_indexes()
