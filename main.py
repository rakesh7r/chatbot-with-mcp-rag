import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = FastAPI()

# ----------------------------
# Types
# ----------------------------
class HistoryItem(BaseModel):
    role: str
    parts: List[Dict[str, str]]

class ChatType(BaseModel):
    prompt: str
    response: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    prompt: str
    history: List[ChatType] = []

class ResponseSchema(BaseModel):
    status: str
    prompt: str
    message: str
    data: Dict[str, Any]

# ----------------------------
# Setup Gemini client
# ----------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

GENERATION_CONFIG = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

SYSTEM_INSTRUCTION = """
You're a helpful assistant designed to provide clear, structured responses.
- Format your responses in valid JSON.
- If applicable, use markdown formatting inside JSON (e.g., for descriptions).
- Be concise but detailed when necessary.

{
  "status": "string (success, error, info)",
  "prompt": "string (original prompt)",
  "message": "string (detailed description of the response)",
  "data": {
    "items" : [
      {
        "name": "string (name of the item)",
        "description": "string (description of the item)"
      }
    ],
    "suggestions": ["string (suggested actions or next steps)"],
    "citations": ["string array (optional, for providing sources or references)"]
  }
}

Use markdown formatting inside JSON (e.g., for description and response).
Suggestions are prompt suggestions for the user based on the previous chats.
Return only best 3 suggestions and citations if any.
All responses must strictly adhere to this structure. Only return JSON—no extra text or explanations.
"""

# ----------------------------
# Utils
# ----------------------------
def parse_history(history: List[ChatType]) -> List[HistoryItem]:
    parsed = []
    for item in history:
        if item.prompt:
            parsed.append({"role": "user", "parts": [{"text": item.prompt}]})
            if item.response:
                parsed.append({"role": "model", "parts": [{"text": item.response.get("message", "")}]})
    return parsed


async def send_message(message: str, history: List[HistoryItem]):
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-lite-preview-02-05",
        generation_config=GENERATION_CONFIG,
        system_instruction=SYSTEM_INSTRUCTION,
    )

    chat = model.start_chat(history=history)
    response = chat.send_message(message)

    return response.text


# ----------------------------
# Routes
# ----------------------------
@app.get("/")
async def root():
    return {"message": "Cognito app!"}


@app.post("/chat")
async def chat(req: ChatRequest):
    try:

        prompt = req.prompt
        history_data = req.history

        parsed_history = parse_history([ChatType(**h) for h in history_data])

        response = await send_message(prompt, parsed_history)

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
