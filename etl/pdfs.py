import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:                
                text += page_text
    pattern = r'([A-Za-zÁÉÍÓÚÑáéíóúñ\s]+:)(.*?)(?=[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+:|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    paragraphs = []
    for match in matches:
        title = match[0].strip() 
        content = match[1].strip() 
        paragraphs.append(f"{title} {content}")
    return paragraphs

# def generate_embeddings(chunks):
#     response = co.embed(texts=chunks, model="large", truncate="RIGHT").embeddings
#     return response

# def insert_embeddings_in_chromadb(collection, chunks, embeddings):
#     for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
#         collection.add(
#             ids = [str(i)], # Added ids argument with unique ID for each chunk
#             documents=[chunk],
#             embeddings=[embedding],
#             metadatas=[{"chunk_id": i}]
#         )

# curr_dir = Path(__file__).parent
# env_path = curr_dir.parent / '.env' 
# datalake_path = curr_dir.parent / 'data' / 'documento.pdf'# os.getenv("DATALAKE_PATH")
# load_dotenv(dotenv_path=env_path, override=True)
# cohere_api_key = os.getenv("COHERE_API_KEY")
# collection_name = os.getenv("CHROMA_COLLECTION_NAME")
# print(collection_name)
# client = chromadb.Client(Settings(is_persistent=True, persist_directory=str(curr_dir)))
# collection = client.get_or_create_collection(collection_name)
# chunks = extract_text_from_pdf(datalake_path)
# co = cohere.Client(cohere_api_key)
# embeddings = generate_embeddings(chunks)
# insert_embeddings_in_chromadb(collection, chunks, embeddings)