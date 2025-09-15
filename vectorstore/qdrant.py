from qdrant_client import QdrantClient
from embed.gemma import get_embedding
from sentence_transformers import SentenceTransformer

embed = SentenceTransformer("intfloat/e5-small-v2")


qdrant_client = QdrantClient(host="localhost", port=6333)

collection_name = "documents"

qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config={"size": 384, "distance": "Cosine"}  # e.g., Sentence-BERT embeddings
)

import uuid

def push_chunks_to_qdrant(chunks):
    # Generate embeddings
    print("Generating embeddings for chunks...")
    vectors = embed.encode(chunks, batch_size=32, show_progress_bar=True).tolist()
    print(f"Generated {len(vectors)} embeddings.")

    # Generate unique IDs for each chunk
    ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
    print(f"Generated {len(ids)} unique IDs.")
    # Prepare points with payloads
    points = [
        {
            "id": id_,
            "vector": vector,
            "payload": {"text": chunk, "chunk_id": i}
        }
        for i, (id_, vector, chunk) in enumerate(zip(ids, vectors, chunks))
    ]
    
    # print("points", points)

    # Push to Qdrant
    qdrant_client.upsert(
        collection_name=collection_name,
        points=points
    )
    print(f"Pushed {len(chunks)} chunks to Qdrant collection '{collection_name}'")


def semantic_search(query: str, top_k: int = 5):
    """
    Perform semantic search in Qdrant for a given query.
    
    Args:
        query (str): The user query.
        top_k (int): Number of top results to return.
    
    Returns:
        list: Search results with payloads and scores.
    """
    # Convert query to vector
    query_vector = embed.encode(query).tolist()
    
    # Search in Qdrant
    results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k
    )
    
    return [
        {
            "id": hit.id,
            "score": hit.score,
            "payload": hit.payload
        }
        for hit in results
    ]