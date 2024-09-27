import cohere
import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from pathlib import Path
from etl.pdfs import extract_text_from_pdf


def generate_embeddings(chunks):
    response = co.embed(texts=chunks, model="large", truncate="RIGHT").embeddings
    return response

def insert_embeddings_in_chromadb(collection, chunks, embeddings):
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids = [str(i)], # Added ids argument with unique ID for each chunk
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{"chunk_id": i}]
        )

curr_dir = Path(__file__).parent
persist_dir = curr_dir / 'app' / 'datavector'
env_path = curr_dir / '.env' 
datalake_path = curr_dir / 'data' 
pdf_path = datalake_path / 'documento.pdf'# os.getenv("DATALAKE_PATH")
load_dotenv(dotenv_path=env_path, override=True)
cohere_api_key = os.getenv("COHERE_API_KEY")
collection_name = os.getenv("CHROMA_COLLECTION_NAME")
print(collection_name)
client = chromadb.Client(Settings(is_persistent=True, persist_directory=str(persist_dir)))
collection = client.get_or_create_collection(collection_name)
chunks = extract_text_from_pdf(pdf_path)
co = cohere.Client(cohere_api_key)
embeddings = generate_embeddings(chunks)
insert_embeddings_in_chromadb(collection, chunks, embeddings)