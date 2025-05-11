import os

import weaviate
from injector import inject
from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_weaviate import WeaviateVectorStore
from weaviate.client import WeaviateClient


@inject
class VectorDatabaseService:
    client: WeaviateClient
    vector_store: WeaviateVectorStore

    def __init__(self):
        self.client = weaviate.connect_to_local(
            host=os.getenv("WEAVIATE_HOST"),
            port=int(os.getenv("WEAVIATE_PORT")),
        )

        self.vector_store = WeaviateVectorStore(
            client=self.client,
            index_name="Dataset",
            text_key="text",
            embedding=QianfanEmbeddingsEndpoint()
        )

    def get_retriever(self) -> VectorStoreRetriever:
        return self.vector_store.as_retriever()

    @classmethod
    def combine_documents(cls, documents: list[Document]) -> str:
        return "\n\n".join([document.page_content for document in documents])
