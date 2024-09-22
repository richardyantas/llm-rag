import cohere
import chromadb
from chromadb.config import Settings

# Inicializar Cohere con tu clave de API (debes obtenerla desde el panel de Cohere)
cohere_api_key = 'CvPKcfibATr60NC4IDP9wIl0kmoBVDyy449ySK59'
cohere_client = cohere.Client(cohere_api_key)

# Crear un cliente de ChromaDB (almacenamiento local por defecto)
chroma_client = chromadb.Client(Settings())

# Crear o conectar a una colección en ChromaDB
collection = chroma_client.create_collection("document_embeddings")

# Función para agregar documentos a la base de datos
def add_documents_to_chromadb(documents):
    # Usar Cohere para generar embeddings de los documentos
    response = cohere_client.embed(texts=documents)
    embeddings = response.embeddings

    # Agregar los documentos y embeddings a ChromaDB
    for i, doc in enumerate(documents):
        collection.add(
            documents=[doc],
            embeddings=[embeddings[i]],
            ids=[str(i)]
        )

# Función para buscar el documento más cercano dado un query
def query_chromadb(query):
    # Generar el embedding del query usando Cohere
    query_embedding = cohere_client.embed(texts=[query]).embeddings[0]

    # Consultar ChromaDB para obtener los documentos más cercanos
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1  # Número de resultados más cercanos que deseas
    )

    return results['documents']

# Ejemplo de uso
if __name__ == "__main__":
    # Lista de documentos para almacenar
    documents = [
        "Python is a powerful programming language.",
        "Cohere provides language models for NLP tasks.",
        "ChromaDB is great for vector database solutions."
    ]
    
    # Agregar los documentos a la base de datos
    add_documents_to_chromadb(documents)
    
    # Consultar ChromaDB con un query
    query = "What is Cohere?"
    closest_documents = query_chromadb(query)
    
    print(f"Closest document to query '{query}': {closest_documents[0]}")
