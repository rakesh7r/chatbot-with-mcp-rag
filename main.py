
from fastapi import FastAPI
from dotenv import load_dotenv
from api.chat import router as chat
from api.yfin import router as yfin


load_dotenv()

app = FastAPI()

app.include_router(chat, prefix="/api", tags=["chat"])
app.include_router(yfin, prefix="/api/yfin", tags=["yfin"])