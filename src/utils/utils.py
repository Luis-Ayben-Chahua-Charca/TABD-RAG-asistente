import os
import chromadb
from unstructured.partition.auto import partition
from collections import Counter

CHROMA_PATH = "chroma_data"
CHROMA_COLLECTION_NAME = "documentos_empresa"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

def vectorizar_documento(filepath):
    filename = os.path.basename(filepath)
    try:
        elements = partition(filename=filepath, languages=["es"])
        chunks = [el.text.strip() for el in elements if el.text and len(el.text.strip()) > 20]

        #supuestamente para auditoria futura
        total = len(elements)
        utiles = len(chunks)
        omitidos = total - utiles
        
        for i, chunk in enumerate(chunks):
            uid = f"{filename}_{i}"
            collection.add(
                ids=[uid],
                documents=[chunk],
                metadatas=[{"source": filename}],
            )

        return f" {filename} vectorizado con {len(chunks)} fragmentos."
    except Exception as e:
        return f" Error procesando {filename}: {e}"

def obtener_documentos_vectorizados():
    # Accede a todos los metadatos y extrae los nombres de archivos únicos
    resultados = collection.get(include=["metadatas"])
    nombres = {meta["source"] for meta in resultados["metadatas"]}
    #print("recuperando documentos")
    return sorted(list(nombres))

def eliminar_documento(nombre_archivo):
    if not resultados["metadatas"]:
        return "⚠️ No hay documentos cargados."
    resultados = collection.get(include=["metadatas", "ids"])
    ids_a_borrar = [doc_id for doc_id, meta in zip(resultados["ids"], resultados["metadatas"])
                    if meta["source"] == nombre_archivo]

    if ids_a_borrar:
        collection.delete(ids=ids_a_borrar)
        return f"🗑️ Se eliminaron {len(ids_a_borrar)} fragmentos de {nombre_archivo}."
    return "⚠️ Documento no encontrado en la colección."


def reindexar_documento(nombre_archivo):
    docs_path = os.path.join("docs", nombre_archivo)
    if os.path.exists(docs_path):
        eliminar_documento(nombre_archivo)
        return vectorizar_documento(docs_path)
    return "⚠️ Archivo no encontrado en 'docs/'"
