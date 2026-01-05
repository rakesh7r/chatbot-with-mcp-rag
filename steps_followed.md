root@ip-172-31-45-2:/home/ubuntu# docker run -d -p 6333:6333 --name qdrant -v qdrant_storage:/qdrant/storage qdrant/qdrant

podman run -d -p 8001:8001 --name mcp-rag mcp-rag


Attached elastic ip so, the public ip doesnt change on instance restarts.