from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from processors.document_processor import LawDocumentProcessor
import os

router = APIRouter()

@router.post("/")
def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join("data", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    processor = LawDocumentProcessor()
    vector_store = processor.process_documents()
    if not vector_store:
        raise HTTPException(status_code=500, detail="Error procesando documentos")

    return {"mensaje": "Documento subido y procesado exitosamente"}