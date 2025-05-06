from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from processors.document_processor import LawDocumentProcessor
from config import SYSTEM_PROMPT
from resumen import create_executive_summary, format_legal_context, get_legal_context
import asyncio

import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")


def init_vector_store():
    processor = LawDocumentProcessor()
    return processor.load_vector_store()

def get_chat_response(prompt, vector_store):
    context = get_legal_context(vector_store, prompt)
    enriched_prompt = f"""
Tipo de consulta: {prompt}

Contexto:
{format_legal_context(context)}
"""

    chat = ChatOpenAI(api_key=API_KEY, model="gpt-4", temperature=0.3)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=enriched_prompt)
    ]
    response = chat.invoke(messages)
    summary = create_executive_summary(response.content)
    return response.content, summary

async def get_streaming_response(prompt, vector_store):
    context = get_legal_context(vector_store, prompt)
    enriched_prompt = f"""
Tipo de consulta: {prompt}

Contexto:
{format_legal_context(context)}
"""

    chat = ChatOpenAI(
        api_key=API_KEY, 
        model="gpt-4o", 
        temperature=0.3,
        streaming=True
    )
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=enriched_prompt)
    ]
    
    response_text = ""
    
    async for chunk in chat.astream(messages):
        if chunk.content:
            response_text += chunk.content
            yield chunk.content, False

    # Cuando termina, enviamos el resumen
    summary_df = create_executive_summary(response_text)
    # Convertir el DataFrame a un formato serializable (diccionario)
    summary = summary_df.to_dict(orient="records")
    
    final_response = {
        'respuesta': response_text,
        'resumen': summary
    }
    yield final_response, True