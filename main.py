
from fastapi import FastAPI
from dotenv import load_dotenv
from api.chat import router as chat
from api.yfin import router as yfin

from langchain.pdf_loader import load_and_split_pdf
from vectorstore.qdrant import push_chunks_to_qdrant, semantic_search


load_dotenv()

# app = FastAPI()

# app.include_router(chat, prefix="/api", tags=["chat"])
# app.include_router(yfin, prefix="/api/yfin", tags=["yfin"])


async def main():
    chunks = await load_and_split_pdf("/Users/rakeshg/Downloads/The Rust Programming Language 13-40.pdf")
    print(f"Loaded and split into {len(chunks)} chunks.")
    push_chunks_to_qdrant(chunks=chunks)
    
    query = "What is the Anatomy of a Rust Program?"
    results = semantic_search(query=query, top_k=5)
    print(f"Search results for query '{query}':", results)
    
    
    

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())