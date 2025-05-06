from fastapi import FastAPI
from routers import chat, upload
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="EcoPoliciApp API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(upload.router, prefix="/upload", tags=["Document Upload"])

@app.get("/status")
def status():
    return {"status": "API funcionando"}