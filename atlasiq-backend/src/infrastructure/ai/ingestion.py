from llama_index.core import VectorStoreIndex, Document
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from pydantic import BaseModel

class DocumentPayload(BaseModel):
    content: str
    metadata: dict

def get_qdrant_client():
    return QdrantClient("localhost", port=6333)

def ingest_document(payload: DocumentPayload):
    """
    Ingests a document into the Qdrant vector store using LlamaIndex.
    """
    client = get_qdrant_client()
    vector_store = QdrantVectorStore(client=client, collection_name="atlasiq_docs")
    
    document = Document(
        text=payload.content,
        metadata=payload.metadata
    )
    
    # In a real app, you would use a pipeline with chunking and embeddings here
    # index = VectorStoreIndex.from_documents([document], vector_store=vector_store)
    return {"status": "success", "message": "Document ingested"}

def retrieve_context(query: str):
    """
    Retrieves relevant context for the RAG agent.
    """
    client = get_qdrant_client()
    vector_store = QdrantVectorStore(client=client, collection_name="atlasiq_docs")
    
    # index = VectorStoreIndex.from_vector_store(vector_store)
    # query_engine = index.as_query_engine()
    # response = query_engine.query(query)
    
    # Stub response
    return "Retrieved context for query: " + query
