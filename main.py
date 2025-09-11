
from fastapi import FastAPI
from dotenv import load_dotenv
from api.chat import router as chat_router

load_dotenv()

app = FastAPI()

app.include_router(chat_router, prefix="/api", tags=["chat"])