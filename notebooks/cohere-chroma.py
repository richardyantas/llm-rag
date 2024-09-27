import cohere
import chromadb
from chromadb.config import Settings

cohere_api_key = 
cohere_client = cohere.Client(cohere_api_key)
chroma_client = chromadb.Client(Settings())

collection = chroma_client.create_collection("document_embeddings")
def add_documents_to_chromadb(documents):
    response = cohere_client.embed(texts=documents)
    embeddings = response.embeddings
    for i, doc in enumerate(documents):
        collection.add(
            documents=[doc],
            embeddings=[embeddings[i]],
            ids=[str(i)]
        )

def query_chromadb(query):
    query_embedding = cohere_client.embed(texts=[query]).embeddings[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1  # Número de resultados más cercanos que deseas
    )

    return results['documents']


if __name__ == "__main__":
    documents = [
        "Python is a powerful programming language.",
        "Cohere provides language models for NLP tasks.",
        "ChromaDB is great for vector database solutions."
    ]
    add_documents_to_chromadb(documents)
    query = "What is Cohere?"
    closest_documents = query_chromadb(query)
    print(f"Closest document to query '{query}': {closest_documents[0]}")
