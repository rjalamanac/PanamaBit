# app.py
import os
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from transformers import pipeline

DATA_PATH = "data/jobs.csv"
EMB_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
QA_MODEL_NAME = "distilbert-base-cased-distilled-squad"  # rápido y ligero

# Cargar CSV
df = pd.read_csv(DATA_PATH, encoding="utf-8")

# Crear campo textual a indexar (puedes ajustar)
df["text_for_index"] = (df["title"].fillna("") + ". " +
                        df["description"].fillna("") + " Requisitos: " +
                        df["requirements"].fillna(""))

# Cargar modelo de embeddings
print("Cargando modelo de embeddings...", EMB_MODEL_NAME)
embedder = SentenceTransformer(EMB_MODEL_NAME)

# Generar embeddings (si ya lo has calculado, podrías persistirlos)
texts = df["text_for_index"].tolist()
embeddings = embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)

# Indexar con FAISS
d = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(embeddings)
print(f"Index creado con {index.ntotal} vectores (dim={d}).")

# Cargar modelo QA
print("Cargando pipeline de QA...", QA_MODEL_NAME)
qa_pipe = pipeline("question-answering", model=QA_MODEL_NAME, tokenizer=QA_MODEL_NAME)

app = Flask(__name__)

def retrieve_top_k(question, k=3):
    q_emb = embedder.encode([question], convert_to_numpy=True)
    D, I = index.search(q_emb, k)
    results = []
    for idx in I[0]:
        row = df.iloc[idx].to_dict()
        results.append({
            "id": int(row["id"]),
            "title": row["title"],
            "employer": row["employer"],
            "location": row["location"],
            "contract_number": row["contract_number"],
            "start_date": row["start_date"],
            "end_date": row["end_date"],
            "description": row["description"],
            "requirements": row["requirements"]
        })
    return results

@app.route("/")
def index_route():
    return "Chatbot QA sobre CSV - servicio en /api/ask"

@app.route("/api/ask", methods=["POST"])
def ask():
    payload = request.json
    if not payload or "question" not in payload:
        return jsonify({"error": "Envía JSON con {'question': 'tu pregunta'}"}), 400
    question = payload["question"]
    top_k = int(payload.get("top_k", 3))

    # Recuperar documentos
    docs = retrieve_top_k(question, k=top_k)

    # Construir contexto concatenando descripciones (cuidado con longitud)
    context = "\n\n".join([f"{d['title']}. {d['description']}. Requisitos: {d['requirements']}" for d in docs])

    # Preparar input para QA
    qa_input = {"question": question, "context": context}

    try:
        ans = qa_pipe(qa_input)
    except Exception as e:
        return jsonify({"error": "Error en pipeline QA", "detail": str(e)}), 500

    response = {
        "question": question,
        "answer": ans.get("answer"),
        "score": float(ans.get("score", 0.0)),
        "context_used": context,
        "docs": docs
    }
    return jsonify(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
