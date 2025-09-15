import asyncio
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


async def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    return pages


async def split_text(pages):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
    )
    texts = []
    for page in pages:
        splits = text_splitter.split_text(page.page_content)
        texts.extend(splits)
    return texts


async def load_and_split_pdf(file_path):
    pages = await load_pdf(file_path)
    chunks = await split_text(pages)
    return chunks

async def main():
    chunks = await load_and_split_pdf("/Users/rakeshg/Downloads/The Rust Programming Language 13-40.pdf")
    print(f"Loaded and split into {len(chunks)} chunks.")


if __name__ == "__main__":
    asyncio.run(main())
