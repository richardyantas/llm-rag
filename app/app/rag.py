from googletrans import Translator
from langdetect import detect
from dotenv import load_dotenv
import cohere
import chromadb
import os
from pathlib import Path
from chromadb.config import Settings

import emoji
from langchain.prompts import PromptTemplate

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

def query_embeddings(question):  # retrieval context (chunk most similar to query embedded)
    question_embedding = co.embed(texts=[question], model="large", truncate="RIGHT").embeddings[0]    
    results = collection.query(query_embeddings=[question_embedding], n_results=1) # Buscar el chunk más similar en ChromaDB
    return results["documents"][0]  # Retorna el chunk más relevante

def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

def create_prompt_translated(user_question, context):
    # Detectar el idioma de la pregunta
    language = detect(user_question)
    prompt = f"""
      Contexto: {context}
      Pregunta: {user_question}

      Instruccion:
      - Responder en solo una oración.
      - Siempre responder en el mismo idioma de la pregunta.
      - Responder en tercera persona.
      - Agrega algunos emojis
      """
    #  Agregar emojis dentro del contenido de la respuesta.
    prompt_lang = translate_text(prompt, language)
    return prompt_lang


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

def create_prompt_translated2(user_question, context):
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
    chain = LLMChain(llm=llm, prompt=prompt) # deprecated
    # Ejemplo de uso
    question = "¿Cuál es la capital de Francia?"
    language = detect(question)
    response = process_question(question, chain)
    return response


def generate_response(question, context):
    # Generar una respuesta utilizando Cohere
    prompt = create_prompt_translated(question, context)

    # work here add langchain to add emojis
    print(prompt)
    #model="command-xlarge"
    response = co.generate(prompt=prompt,
                           max_tokens=50,  # Ajusta el número de tokens según sea necesario
                           temperature=0.5 # Ajusta la temperatura para variar la creatividad
                           ).generations[0].text
    return response


def generate_answer(question):
    # question = "Qual è il nome del fiore magico?"
    relevant_chunk = query_embeddings(question)    
    response = generate_response(question, relevant_chunk)
    print(response)
    # print(detect(response)) # error
    return response

# question = "Qual è il nome del fiore magico?"
# relevant_chunk = query_embeddings(question)    
# response = generate_response(question, relevant_chunk)
# print(response)
# # print(detect(response))