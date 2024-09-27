# from googletrans import Translator
import cohere
import chromadb
import os
import emoji
from langdetect import detect
from dotenv import load_dotenv
from pathlib import Path
from chromadb.config import Settings
from langchain.prompts import PromptTemplate

curr_dir = Path(__file__).parent
env_path = curr_dir.parent.parent / '.env'
vectordatabase_path = curr_dir.parent / 'datavector'
load_dotenv(dotenv_path=env_path, override=True)
cohere_api_key = os.getenv("COHERE_API_KEY")
collection_name = os.getenv("CHROMA_COLLECTION_NAME")
client = chromadb.Client(Settings(is_persistent=True, persist_directory=str(vectordatabase_path)))
collection = client.get_collection(collection_name)
co = cohere.Client(cohere_api_key)

def query_embeddings(question):  # retrieval context (chunk most similar to query embedded)
    question_embedding = co.embed(texts=[question], model="large", truncate="RIGHT").embeddings[0]    
    results = collection.query(query_embeddings=[question_embedding], n_results=1) # Buscar el chunk más similar en ChromaDB
    return results["documents"][0]  # Retorna el chunk más relevante

def translate_text(text, target_language):
    # translator = Translator()
    # translated = translator.translate(text, dest=target_language)
    # return translated.text
    return text

languages = {
    "en": "english",
    "es": "español",
    "pt": "Português"
} 

def create_prompt_translated(user_question, context):
    language = detect(user_question)
    prompt = f"""
      Contexto: {context}
      Pregunta: {user_question}
      Instruccion:
      - Responder en solo una oración.
      - Siempre responder en el idioma {languages[language]}.
      - Responder en tercera persona.
      - Reemplaza algunos palabras por emojis que resuman la oración
      """
    
    print("prompt:", prompt)
    return prompt


predefined_answers = {
    "¿quien es zara?": "Zara 🚀 es un explorador intrépido y valiente 🏃♂️🏹, que viaja en busca de la paz para su galaxy 🌌, en la lejana galaxia de"
}

def add_emojis(text):
    return emoji.emojize(text, use_aliases=True)

def generate_response(question, context):
    if question in predefined_answers:
        return predefined_answers[question]    
    prompt = create_prompt_translated(question, context)    
    response = co.generate(prompt=prompt,
                           max_tokens=50,  # Ajusta el número de tokens según sea necesario
                           temperature=0.5 # Ajusta la temperatura para variar la creatividad
                           ).generations[0].text
    # response = add_emojis(response)
    predefined_answers[question] = response
    return response


def generate_answer(question):
    relevant_chunk = query_embeddings(question)    
    response = generate_response(question, relevant_chunk)
    print(response)
    return response

# question = "Qual è il nome del fiore magico?"
# question = "¿O que Zara está fazendo?"
# print(detect(question))
# response = generate_answer(question)
# print(response)
# print(detect(response))