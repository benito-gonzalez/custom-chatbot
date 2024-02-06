from llama_index.llms import OpenAI
from llama_index.embeddings import OpenAIEmbedding


class EmbeddingModelManager:

    @staticmethod
    def get_embedding_model():
        return OpenAIEmbedding(model='text-embedding-3-small')


class TextModelManager:

    @staticmethod
    def get_llm():
        return OpenAI("gpt-3.5-turbo", temperature=0, max_tokens=256)
