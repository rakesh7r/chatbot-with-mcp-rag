from fastapi import APIRouter, Request, UploadFile, HTTPException, File
from fastapi.responses import JSONResponse
from schema.chat import ChatRequest, ChatType
from llm.gemini import gemini_client
import json
from typing import List
from langchain.pdf_loader import load_and_split_pdf


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Cognito app!"}

@router.post("/chat")
async def chat(req: ChatRequest):
    try:
        prompt = req.prompt
        history_data = req.history
        parsed_history = gemini_client.parse_history([ChatType(**h) for h in history_data])
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
    print(f"Received file: {file.filename}")
    chunks = await load_and_split_pdf(file.file)
    print(f"Loaded and split into {len(chunks)} chunks.")
    return {"filename": file.filename, "chunks": len(chunks)}
    