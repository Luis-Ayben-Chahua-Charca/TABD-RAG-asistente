#  Asistente RAG - Retrieval-Augmented Generation para Documentos Empresariales

Este proyecto implementa un **asistente inteligente** que permite consultar documentos institucionales usando técnicas de **vectorización semántica (ChromaDB)** y modelos de lenguaje como **Mistral** a través de **Ollama**.

---

## Características

- Subida y vectorización automática de archivos `.pdf`, `.docx`, `.txt`, `.md`
- Consulta semántica usando Large Language Models (LLMs) vía Ollama
- Interface web con Flask y Bootstrap
- OCR automático si el PDF no tiene texto
- Gestión de documentos: subir, eliminar, reindexar
- Persistencia con ChromaDB local

---

##  Requisitos

### Requisitos comunes (para ambos métodos)

- [Ollama] instalado y funcionando
  ```bash
  ollama run mistral
  ```
- Conexión a internet para descargar el modelo al menos una vez

---

## 🐳 OPCIÓN 1: Ejecutar con Docker Compose (Linux o Windows)

### 1. Clona el proyecto

```bash
git clone https://github.com/Luis-Ayben-Chahua-Charca/TABD-asistente-RAG.git
cd asistente-rag
```

### 2. Ejecuta Ollama en otra terminal

```bash
ollama run mistral
```

### 3. Construye y ejecuta el contenedor

```bash
docker-compose up --build
```

 El sistema montará volúmenes para:

- `./docs`: documentos subidos
- `./chroma_data`: base de vectores persistente

### 4. Accede en tu navegador

```
http://localhost:5000
```

---

##  OPCIÓN 2: Ejecutar sin Docker (entorno nativo)

###  Linux

```bash
sudo apt update
sudo apt install tesseract-ocr poppler-utils python3 python3-venv
```

###  Windows

1. Instala [Python](https://www.python.org/downloads/windows/)
2. Instala Tesseract con [Chocolatey](https://chocolatey.org/install)

```powershell
choco install tesseract poppler
```

---

### 1. Clona y crea entorno virtual

```bash
git clone https://github.com/Luis-Ayben-Chahua-Charca/TABD-asistente-RAG.git
cd asistente-rag

python -m venv venv
# Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

---

### 2. Instala dependencias

```bash
pip install -r requirements.txt
pip install "unstructured[pdf]"  
```

---
<>
### 3. Ejecuta Ollama en otra terminal

```bash
ollama run mistral
```

---

### 4. Corre la aplicación Flask

```bash
python run.py
```

Y accede en [http://localhost:5000](http://localhost:5000)

---

## 📁 Estructura del Proyecto

```
asistente-rag/
├── run.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── docs/                
├── chroma_data/         
├── src/
│   ├── app.py
│   ├── config.py
│   ├── routes/
│   ├── services/
│   ├── templates/
│   └── static/
```

---



##  Autor

Luis Ayben Chahua Charca  
Curso: *Tópicos Avanzados de Bases de Datos*

---

##  Licencia

libre para uso académico o personal
