# Dockerfile (CPU)
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# dependencias del sistema (faiss y otras)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl wget ffmpeg libsndfile1 \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# copiar requirements y código
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# copiar app
COPY . /app

# Exponer puerto
EXPOSE 5000

CMD ["python", "app.py"]
