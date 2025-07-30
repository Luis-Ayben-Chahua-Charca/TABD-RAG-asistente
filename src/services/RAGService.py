from database.chroma_client import get_chroma_client
from chromadb.utils import embedding_functions
import subprocess
import time

COLLECTION_NAME = "documentos_empresa"

# Inicializa función de embedding
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

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
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        capture_output=True,
        timeout=60
    )
    return result.stdout.decode().strip()


def handle_query(question: str) -> dict:
    inicio = time.perf_counter()

    context = retrieve_context(question)
    prompt = build_prompt(question, context)
    respuesta = generate_response(prompt)

    duracion = time.perf_counter() - inicio
    return {
        "respuesta": respuesta,
        "tiempo": f"{duracion:.2f} segundos"
    }