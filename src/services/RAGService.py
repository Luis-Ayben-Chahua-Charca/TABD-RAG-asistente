from database.chroma_client import get_chroma_client
from chromadb.utils import embedding_functions
import subprocess
import requests
import time

COLLECTION_NAME = "documentos_empresa"

# Inicializa función de embedding
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def rewrite_query(question: str) -> str:
    prompt = f"""Reescribe la siguiente pregunta para que sea más clara, específica y útil para buscar información en documentos técnicos o institucionales.

Pregunta original:
{question}

Pregunta reformulada:"""

    response = requests.post(
        "http://host.docker.internal:11434/api/generate",  # ← usa Ollama desde el host
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()

def retrieve_context(question: str, k: int = 5) -> str:
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    results = collection.query(
        query_texts=[question],
        n_results=k
    )
    docs = results['documents'][0]
    return "\n\n".join(docs)


def build_prompt(question: str, context: str) -> str:
    return f"""Responde la siguiente pregunta basándote únicamente en el contexto proporcionado.

### Contexto:
{context}

### Pregunta:
{question}

### Respuesta:"""


def generate_response(prompt: str, model: str = "mistral") -> str:
    response = requests.post(
        "http://host.docker.internal:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()


def handle_query(question: str) -> dict:
    inicio = time.perf_counter()

    pregunta_reescrita = rewrite_query(question)
    context = retrieve_context(pregunta_reescrita)
    prompt = build_prompt(question, context)
    respuesta = generate_response(prompt)

    duracion = time.perf_counter() - inicio
    return {
        "respuesta": respuesta,
        "tiempo": f"{duracion:.2f} segundos",
        "pregunta_reescrita": pregunta_reescrita
    }