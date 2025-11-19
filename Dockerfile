# Imagen base ligera de Python
FROM python:3.11-slim

# Ajustes básicos
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Dependencias de sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiamos los requisitos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos TODO el código de la app
COPY . .

# Exponemos el puerto interno
EXPOSE 8000

# Comando para arrancar gunicorn con tu Flask app
# app:app = archivo app.py, objeto Flask llamado app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
