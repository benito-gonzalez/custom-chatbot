import logging
import chromadb
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    set_global_service_context
)
from typing import List
from llama_index.vector_stores import ChromaVectorStore
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
APP_PATH = os.path.join(my_path, "..", "..")
DOCUMENTS_PATH = os.path.join(APP_PATH, "scraper", "documents")
DB_PATH = os.path.join(APP_PATH, "chroma_db")

os.environ['OPENAI_API_KEY'] = st.secrets["api_crendentials"]
openai.api_key = st.secrets.api_crendentials


def get_service_context():
    embedding_model = EmbeddingModelManager.get_embedding_model()
    llm = TextModelManager.get_llm()
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embedding_model)
    set_global_service_context(service_context)

    return service_context


def check_empty_dir(path: str) -> int:
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


def generate_indexes() -> None:
    for topic in Topics:
        logging.info(f"Starting the document loading for {topic.value.capitalize()}...")
        pending_dir = os.path.join(DOCUMENTS_PATH, topic.value, "pending")

        if check_empty_dir(pending_dir):
            logging.info(f"There is no new documents for {topic.value.capitalize()}")
        else:
            # load the documents in /pending directory
            documents = SimpleDirectoryReader(pending_dir).load_data()

            # initialize client, setting path to save data
            db = chromadb.PersistentClient(path=DB_PATH)
            # create collection
            chroma_collection = db.get_or_create_collection("Collection_" + topic.value)
            # assign chroma as the vector_store to the context
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            service_context = get_service_context()

            logging.info("Starting the indexing process...")
            VectorStoreIndex.from_documents(documents, service_context=service_context,
                                            storage_context=storage_context)

            move_processed_documents(documents, topic)


@st.cache_resource
def load_indexes(topic: Topics) -> VectorStoreIndex:
    logging.info(f"Loading indexes for {topic.value.capitalize()}...")

    # initialize client
    db = chromadb.PersistentClient(path=DB_PATH)

    # get collection
    chroma_collection = db.get_or_create_collection("Collection_" + topic.value)

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    service_context = get_service_context()

    # load your index from stored vectors
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context, service_context=service_context
    )
    return index


if __name__ == "__main__":
    generate_indexes()
