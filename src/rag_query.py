"""
This script demonstrates a simple retrieval-augmented generation (RAG) approach for answering customer support queries based on a product catalog.
It uses a vector database to find relevant context and then generates responses using a language model.
"""
import os
import ollama
import chromadb
from sentence_transformers import SentenceTransformer

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
ollama_client = ollama.Client(host=OLLAMA_HOST)

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

chroma_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chroma_db")
client = chromadb.PersistentClient(path=str(chroma_path))
collection = client.get_or_create_collection(name="e-shop-catalog")

if collection.count() == 0:
    print("WARRNING: collection is empty! First run `cd ..` `python src/index_data.py`.\n")

def find_context(
    query: str,
    number_of_results: int = 3
):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=number_of_results
    )

    documents = results["documents"][0]
    metadata = results["metadatas"][0]
    distances = results["distances"][0]

    return list(zip(documents, metadata, distances))

distance_threshold = 20.00

def create_prompt(
        query: str,
        found_documents
) -> str:
    context_blocks = []
    for text, meta, _ in found_documents:
        context_blocks.append(f"[{meta['name']}]\n{text}")

    context = "\n\n".join(context_blocks)

    prompt = f"""
                Jsi zákaznická podpora e-shopu. Odpovídej VÝHRADNĚ na základě
                níže uvedeného kontextu. Je PŘÍSNĚ ZAKÁZÁNO doplňovat jakékoliv
                informace, dohady, odhady nebo obecné znalosti, které v kontextu
                nejsou doslova uvedené - a to ani jako "pravděpodobně" nebo
                "mělo by". Pokud odpověď v kontextu není, napiš přesně jednu větu:
                "Tuto informaci bohužel nemám k dispozici, doporučuji kontaktovat
                zákaznickou podporu." a nic víc nedodávej.
                
                KONTEXT:
                {context}
                
                DOTAZ ZÁKAZNÍKA:
                {query}
                
                ODPOVĚĎ:
            """
    return prompt

def ask(
        query: str,
        model_llm: str = "qwen2.5:14b"
) -> str:
    found = find_context(query)

    print("Context found (for debugging/transparency):")
    for text, meta, distance in found:
        print(f"[{meta['name']}] (distance: {distance:.3f})")
    print("____________________________________________________________")

    best_distance = found[0][2]
    if best_distance > distance_threshold:
        return (
            "Tuto informaci bohužel nemám k dispozici, doporučuji "
            "kontaktovat zákaznickou podporu."
        )

    prompt = create_prompt(query, found)

    response = ollama.chat(
        model=model_llm,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        options={"temperature": 0.1},
    )

    return response["message"]["content"]

if __name__ == "__main__":
    test_queries = [
        "Jak dlouho vydrží baterie sluchátek SoundMax?",
        "Do kdy můžu vrátit zboží, které jsem si objednal online?",
        "Umí ten notebook hrát Fortnite na ultra?",
    ]

    for query in test_queries:
        print(f"Query: {query}\n")
        print(ask(query))
        print("\n" + "=" * 60 + "\n")