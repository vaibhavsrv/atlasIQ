import os
from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex, Document, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore

class DocumentRAGService:
    def __init__(self):
        # We use a local Qdrant storage to avoid complex Docker setups during this phase.
        qdrant_path = os.path.join(os.getcwd(), "qdrant_data")
        os.makedirs(qdrant_path, exist_ok=True)
        self.client = QdrantClient(path=qdrant_path)
        
    def ingest_document(self, project_id: str, content: str, doc_id: str):
        """Ingests raw text into the vector store under a specific collection (project)."""
        # Ensure collection exists
        collection_name = f"project_{project_id}".replace("-", "_")
        
        vector_store = QdrantVectorStore(client=self.client, collection_name=collection_name)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        doc = Document(text=content, metadata={"doc_id": doc_id, "project_id": project_id})
        
        # Build index from the document
        VectorStoreIndex.from_documents(
            [doc],
            storage_context=storage_context,
        )
        return True

    def query_project_documents(self, project_id: str, query_str: str) -> str:
        """Retrieves context from project documents using semantic search."""
        collection_name = f"project_{project_id}".replace("-", "_")
        
        # Check if collection exists implicitly by trying to connect
        try:
            vector_store = QdrantVectorStore(client=self.client, collection_name=collection_name)
            index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
            
            # Use retriever to fetch top 2 relevant chunks
            retriever = index.as_retriever(similarity_top_k=2)
            nodes = retriever.retrieve(query_str)
            
            if not nodes:
                return ""
            
            context = "\n---\n".join([n.text for n in nodes])
            return context
        except Exception as e:
            # Collection might not exist or be empty
            return ""
