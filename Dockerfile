FROM python:3.12-slim

# Instala OCR, libGL (para procesamiento de PDF con imagen) y otras herramientas necesarias
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia todo el proyecto
COPY . .

# Establece PYTHONPATH para que Python encuentre 'app' dentro de src/
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 5000

CMD ["python", "run.py"]
