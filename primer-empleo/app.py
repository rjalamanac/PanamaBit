from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model and preprocessing tools
clf = joblib.load("Model/xgb_model.pkl")
ohe = joblib.load("Model/encoder.pkl")
scaler = joblib.load("Model/scaler.pkl")
le = joblib.load("Model/label_encoder.pkl")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Request schema
class UserProfile(BaseModel):
    name: str
    age: int
    user_city: str
    has_car: bool
    education_level: str
    english: bool
    studies: str
    job_city: str
    contract_type: str

app = FastAPI()

@app.post("/recommend")
def recommend(user: UserProfile):
    try:
        print("Im here")
        # Transform inputs
        X_text = embedder.encode([user.studies], convert_to_numpy=True)
        X_cat = ohe.transform([[user.education_level, user.english,
                                user.user_city, user.job_city,
                                user.has_car, user.contract_type]])
        X_num = scaler.transform([[user.age]])
        X = np.hstack([X_text, X_cat.toarray(), X_num])
        print("Im here 2")
        # Predict top-3
        probs = clf.predict_proba(X)[0]
        top3_idx = np.argsort(probs)[-3:][::-1]
        top3_jobs = le.inverse_transform(top3_idx)
        top3_scores = probs[top3_idx]

        print("Im here 3")
        return {
            "recommendations": [
                {"job": job, "score": float(score)}
                for job, score in zip(top3_jobs, top3_scores)
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
