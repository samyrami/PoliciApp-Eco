from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.chat_service import get_chat_response, init_vector_store, get_streaming_response
import asyncio
import json

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/")
def chat_endpoint(request: ChatRequest):
    vector_store = init_vector_store()
    if not vector_store:
        raise HTTPException(status_code=500, detail="Vector store no disponible")

    response, summary = get_chat_response(request.query, vector_store)
    return {"respuesta": response, "resumen": summary}

@router.get("/stream")
async def stream_chat_endpoint(query: str):
    vector_store = init_vector_store()
    if not vector_store:
        raise HTTPException(status_code=500, detail="Vector store no disponible")
        
    async def event_generator():
        async for chunk, is_final in get_streaming_response(query, vector_store):
            if is_final:
                yield f"data: {json.dumps({'content': chunk, 'done': True})}\n\n"
            else:
                yield f"data: {json.dumps({'content': chunk, 'done': False})}\n\n"
                await asyncio.sleep(0.05)  # Pequeña pausa para el efecto de typing
        
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )