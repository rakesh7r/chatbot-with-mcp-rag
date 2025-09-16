
from fastapi import FastAPI
from dotenv import load_dotenv
from api.chat import router as chat
from api.yfin import router as yfin

from langchain.pdf_loader import load_and_split_pdf
from vectorstore.qdrant import push_chunks_to_qdrant, semantic_search
from llm.gemini import gemini_client
from mcp_tools.server import router as mcp_router

load_dotenv()

app = FastAPI()

app.include_router(chat, prefix="/api", tags=["chat"])
app.include_router(yfin, prefix="/api/yfin", tags=["yfin"])
app.include_router(mcp_router, prefix="/api/mcp", tags=["mcp"])
