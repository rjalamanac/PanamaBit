# Chatbot CSV -> QA (HF) - proyecto

## Requisitos
- Docker (opcional)
- Python 3.12 (si ejecutas localmente)
- VSCode (recomendado)

## Pasos rápidos (local)
1. Crear entorno y deps:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Generar CSV:
   python generate_csv.py

3. Ejecutar app:
   python app.py
   -> http://localhost:5000

4. Probar endpoint:
   POST http://localhost:5000/api/ask
   JSON: {"question": "¿Qué contratos hay para sindicato?", "top_k": 3}

## Usando Docker
docker build -t chatbot-csv-qa:latest .
docker run --rm -p 5000:5000 -v $(pwd)/data:/app/data chatbot-csv-qa:latest
