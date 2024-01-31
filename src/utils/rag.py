from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
    set_global_service_context
)
from llama_index.llms import OpenAI, Replicate
from llama_index.llms.llama_utils import (
    messages_to_prompt,
    completion_to_prompt,
)
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from llama_index.embeddings import OpenAIEmbedding
from huggingface_hub import login
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


# inject custom system prompt into llama-2
def custom_completion_to_prompt(completion: str) -> str:
    return completion_to_prompt(
        completion,
        system_prompt=(
            "You are a Q&A assistant. Your goal is to answer questions as "
            "accurately as possible is the instructions and context provided."
        ),
    )


def get_service_context(model):
    model_params = {
        Models.GPT: {"model": "gpt-3.5-turbo", "temperature": 0, "max_tokens": 256},
        Models.LLAMA2: {
            "model": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
            "temperature": 0.01,
            # override max tokens since it's interpreted
            # as context window instead of max tokens
            "context_window": 4096,
            # override completion representation for llama 2
            "completion_to_prompt": custom_completion_to_prompt,
            # if using llama 2 for data agents, also override the message representation
            "messages_to_prompt": messages_to_prompt,
        }
    }
    model_params_current = model_params.get(model, {})
    if model == Models.GPT:
        llm = OpenAI(**model_params_current)
        embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    else:
        llm = Replicate(**model_params_current)
        login(st.secrets["hugging_face_token"])
        embed_model = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en-v1.5")

    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
    set_global_service_context(service_context)

    return service_context


def generate_indexes():
    for model in Models:
        if model == Models.LLAMA2:
            continue
        for topic in Topics:
            print(f"Starting the document loading for {topic.value} in {model.value}...")
            documents = SimpleDirectoryReader(os.path.join(DOCUMENTS_PATH, topic.value)).load_data()
            service_context = get_service_context(model)

            print("Starting the indexing process...")
            index = VectorStoreIndex.from_documents(documents, service_context=service_context)

            print("storing the index to disk")
            dir = create_directory(model.value, topic.value)
            index.storage_context.persist(persist_dir=dir)


@st.cache_resource
def load_indexes(model, topic):
    storage_context = StorageContext.from_defaults(persist_dir=os.path.join(STORAGE_PATH, model.value, topic.value))
    service_context = get_service_context(model)
    return load_index_from_storage(storage_context, service_context=service_context)


if __name__ == "__main__":
    generate_indexes()
