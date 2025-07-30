import os
from unstructured.partition.auto import partition
from database.chroma_client import get_chroma_client
import time

# Nombre de colección
COLLECTION_NAME = "documentos_empresa"

def vectorizar_documento(filepath):
    inicio = time.perf_counter()
    filename = os.path.basename(filepath)
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    print(f" Procesando: {filepath}")
    try:
        elements = partition(filename=filepath, languages=["es"])
        chunks = [el.text.strip() for el in elements if el.text and len(el.text.strip()) > 20]

        for i, chunk in enumerate(chunks):
            uid = f"{filename}_{i}"
            collection.add(
                ids=[uid],
                documents=[chunk],
                metadatas=[{"source": filename}],
            )
        duracion = time.perf_counter() - inicio
        return f" {filename} vectorizado con {len(chunks)} fragmentos, en {duracion:.2f} segundos "
    except Exception as e:
        return f" Error procesando {filename}: {e}"


def obtener_documentos_vectorizados():
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    resultados = collection.get(include=["metadatas"])

    nombres = {meta["source"] for meta in resultados["metadatas"]}
    return sorted(list(nombres))


def eliminar_documento(nombre_archivo):
    client = get_chroma_client()
    collection = client.get_or_create_collection(name="documentos_empresa")

    resultados = collection.get(include=["metadatas"])
    ids = resultados["ids"]

    ids_a_borrar = [
        doc_id for doc_id, meta in zip(ids, resultados["metadatas"])
        if meta["source"] == nombre_archivo
    ]

    if ids_a_borrar:
        collection.delete(ids=ids_a_borrar)

        ruta_archivo = os.path.join("docs", nombre_archivo)
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)

        return f" Se eliminaron {len(ids_a_borrar)} fragmentos y el archivo '{nombre_archivo}'."

    return "⚠️ Documento no encontrado en la colección."


def reindexar_documento(nombre_archivo):
    ruta = os.path.join("docs", nombre_archivo)
    if os.path.exists(ruta):
        eliminar_documento(nombre_archivo)
        return vectorizar_documento(ruta)
    return "⚠️ Archivo no encontrado en 'docs/'"
