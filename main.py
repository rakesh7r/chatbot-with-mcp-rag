import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from schema.chat import ChatRequest, ChatType
from dotenv import load_dotenv
import google.generativeai as genai
from llm.gemini import gemini_client

load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Cognito app!"}


@app.post("/chat")
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
