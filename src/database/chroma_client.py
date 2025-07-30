import chromadb
from flask import current_app

_client = None

def get_chroma_client():
    global _client
    if _client is None:
        chroma_path = current_app.config["CHROMA_PATH"]
        _client = chromadb.PersistentClient(path=chroma_path)
    return _client
