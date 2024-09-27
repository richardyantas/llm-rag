from langchain.prompts import PromptTemplate
# from langchain.llms import Cohere
from langchain.memory import ConversationBufferMemory
import langdetect
import emoji
from dotenv import load_dotenv
import cohere
import chromadb
import os
from pathlib import Path
from chromadb.config import Settings

curr_dir = Path(__file__).parent
print(curr_dir)
env_path = curr_dir.parent.parent / '.env'
print(env_path)
vectordatabase_path = curr_dir.parent.parent / 'etl'
print(vectordatabase_path)
load_dotenv(dotenv_path=env_path, override=True)
cohere_api_key = os.getenv("COHERE_API_KEY")
collection_name = os.getenv("CHROMA_COLLECTION_NAME")
print(collection_name)
client = chromadb.Client(Settings(is_persistent=True, persist_directory=str(vectordatabase_path)))
collection = client.get_collection(collection_name)
co = cohere.Client(cohere_api_key)


predefined_answers = {
    "¿Cuál es la capital de Francia?": "La capital de Francia es París. 🗼🇫🇷",
    "What is the capital of France?": "The capital of France is Paris. 🗼🇫🇷",
    "Qual é a capital da França?": "A capital da França é Paris. 🗼🇫🇷"
}

def add_emojis(text):
    return emoji.emojize(text, use_aliases=True)

def process_question(question, chain):    
    if question in predefined_answers:
        return predefined_answers[question]    
    # Generar una respuesta en función del idioma detectado
    response_text = chain.run(question)
    response_with_emojis = add_emojis(response_text)
    return response_with_emojis


def query_embeddings(question):  # retrieval context (chunk most similar to query embedded)
    question_embedding = co.embed(texts=[question], model="large", truncate="RIGHT").embeddings[0]    
    results = collection.query(query_embeddings=[question_embedding], n_results=1) # Buscar el chunk más similar en ChromaDB
    return results["documents"][0]  # Retorna el chunk más relevante


def apply_prompt(question):
    relevant_chunk = query_embeddings(question)    
    # (ingles, # espanol, portugues).
    template = """
    La respuesta a la siguiente pregunta debe ser breve, en una sola oración, en idioma {language} en tercera persona, y agregar emojis relacionados con el contenido:
    Contexto: {context}
    Pregunta: {question}
    Respuesta:
    """
    prompt = PromptTemplate(input_variables=["question", "context", "language"], template=template)
    llm = cohere(api_key=cohere_api_key, model="command-xlarge-nightly", temperature=0.5, max_tokens=100)
    chain = LLMChain(llm=llm, prompt=prompt)
    # Ejemplo de uso
    question = "¿Cuál es la capital de Francia?"
    language = langdetect.detect(question)
    response = process_question(question, chain)
    # print(response)
    return response
