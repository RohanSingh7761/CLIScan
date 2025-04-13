import chromadb
from chromadb.config import Settings
import os
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "./chroma_data"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="threats")

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_code(content):
    return model.encode([content])[0]

def store_threat(content, metadata=None):
    embedding = embed_code(content)
    collection.add(
        documents=[content],
        embeddings=[embedding],
        ids=[str(hash(content))],
        metadatas=[metadata or {}]
    )

def get_similar_threats(content, threshold=0.8):
    embedding = embed_code(content)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    # Basic similarity check using cosine distance
    similar_docs = results["documents"][0]
    if similar_docs:
        return similar_docs
    return []
