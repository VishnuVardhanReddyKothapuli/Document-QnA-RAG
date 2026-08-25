from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from app.services import rag_service

app = FastAPI(title="GenAI PDF Q&A")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("app/uploads", exist_ok=True)
os.makedirs("app/static", exist_ok=True)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("app/static/index.html")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_path = os.path.join("app/uploads", file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        rag_service.process_pdf(file_path)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return JSONResponse(content={"message": f"Successfully processed {file.filename}. You can now start asking questions!"})
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = rag_service.chat(request.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
