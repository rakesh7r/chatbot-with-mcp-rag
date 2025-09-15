import google.generativeai as genai
import os
from dotenv import load_dotenv
from schema.chat import ChatType, HistoryItem
from typing import List

from vectorstore.qdrant import semantic_search


load_dotenv()


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

GENERATION_CONFIG = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

RAG_SYSTEM_INSTRUCTION = """
  You are an AI assistant that answers questions based on provided context documents.
  - Only use the context to answer the question.
  - If the answer is not in the context, say you don’t know.
  - Keep answers concise, factual, and well-structured.
  - Do not invent information beyond the given context.
"""


class GeminiClient: 
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiClient, cls).__new__(cls)
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        return cls._instance
      
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-lite-preview-02-05",
            generation_config=GENERATION_CONFIG,
            system_instruction=SYSTEM_INSTRUCTION,  # ✅ system instruction goes here
            tools=[]
        )
        self.rag_model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-lite-preview-02-05",
            generation_config=GENERATION_CONFIG,
            system_instruction=RAG_SYSTEM_INSTRUCTION, 
            tools=[]
        )

    def parse_history(self, history: List[ChatType]) -> List[HistoryItem]:
        parsed = []
        for item in history:
            if item.prompt:
                parsed.append({"role": "user", "parts": [{"text": item.prompt}]})
                if item.response:
                    parsed.append({"role": "model", "parts": [{"text": item.response.get("message", "")}]})
        return parsed
    
    async def send_message(self, message: str, history: List[HistoryItem]):
        chat = self.model.start_chat(history=history)
        response = chat.send_message(message)
        return response.text
      
    async def rag_answer(self, query: str, top_k: int = 5):
        """
        Runs semantic search + passes results to Gemini for final answer.
        """
        # Step 1: Retrieve docs from Qdrant
        search_results = semantic_search(query, top_k=top_k)
      
        # Step 2: Extract text from payloads
        context_docs = "\n\n".join(
            [doc["payload"].get("text", "") for doc in search_results if doc["payload"]]
        )
      
        # Step 3: Construct prompt (as user role only)
        prompt = f"""
        Context documents:
        {context_docs}
        
        User query:
        {query}
        
        Answer:
        """

        response = self.rag_model.generate_content(
            contents=[{"role": "user", "parts": [prompt]}] 
        )
        return response.text


gemini_client = GeminiClient()