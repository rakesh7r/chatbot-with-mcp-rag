from fastapi import APIRouter, Request, UploadFile, HTTPException, File
from fastapi.responses import JSONResponse
from app.schema.chat import ChatRequest, ChatType
from app.llm.gemini import gemini_client
import json
from typing import List
from app.langchain.pdf_loader import load_and_split_pdf
import tempfile
from app.vectorstore.qdrant import push_chunks_to_qdrant

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Cognito app!"}

def parse_history( history_data: List[ChatType]):
    parsed = []
    for h in history_data:
        parsed.append({
            "role": "user",
            "parts": [{"text": h.prompt}]
        })
        if h.response:
            parsed.append({
                "role": "model",
                "parts": [{"text": h.response}]
            })
    return parsed


@router.post("/chat")
async def chat(req: ChatRequest):
    try:
        prompt = req.prompt
        history_data = req.history
        parsed_history = parse_history(history_data=history_data)
        response = await gemini_client.send_message(prompt, parsed_history)
        if response:
            return JSONResponse(content=json.loads(response), status_code=200)
        else:
            return JSONResponse(
                content={
                    "status": "error",
                    "prompt": prompt,
                    "message": "No response from the model",
                    "data": {"items": [], "suggestions": [], "citations": []},
                },
                status_code=200,
            )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
        
    print(f"Received file: {file.filename}")
    print("temp_path", tmp_path)
    chunks = await load_and_split_pdf(tmp_path)
    print(f"Loaded and split into {len(chunks)} chunks.")
    
    push_chunks_to_qdrant(chunks=chunks)
    return {"filename": file.filename, "chunks": len(chunks)}
    
@router.post("/file-chat")
async def file_chat(req: ChatRequest):
    try:
        prompt = req.prompt
        history_data = req.history
        parsed_history = parse_history(history_data=history_data)
        response = await gemini_client.rag_answer(query=prompt, top_k=5)
        if response:
            return JSONResponse(content=json.loads(response), status_code=200)
        else:
            return JSONResponse(
                content={
                    "status": "error",
                    "prompt": prompt,
                    "message": "No response from the model",
                    "data": {"items": [], "suggestions": [], "citations": []},
                },
                status_code=200,
            )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)