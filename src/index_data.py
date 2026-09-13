"""
This file is used to index the documents in the catalog into a ChromaDB collection.
"""

import os
import sys
import chromadb
from sentence_transformers import SentenceTransformer
sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)
from data.catalog import get_documention

print("Loading embedding model...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="e-shop-catalog")

def index_documents():
    documents = get_documention()

    ids = [document["id"] for document in documents]
    texts = [document["description"] for document in documents]

    metadata = [
        {
            "typ": document["typ"],
            "name": document["title"]
        } for document in documents
    ]

    print(f"Counting embeddings for {len(texts)} documents...")

    embeddings = model.encode(texts).tolist()

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadata
    )

    print(f"Done. In collection there are {collection.count()} documents.")

if __name__ == "__main__":
    index_documents()