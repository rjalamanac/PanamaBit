# prototype_model_xgb.py
import pandas as pd
import numpy as np
import scipy.sparse as sp
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder
import joblib



# Load dataset
df = pd.read_csv("historic.csv")

# -------------------------------
# Sentence Embeddings for studies
# -------------------------------
embedder = SentenceTransformer("all-MiniLM-L6-v2")
X_text = embedder.encode(df["studies"].fillna(""), convert_to_numpy=True)

# One-hot encode categorical features
ohe = OneHotEncoder()
X_cat = ohe.fit_transform(df[[
    "education_level", "english", "user_city", "job_city", "has_car", "contract_type"
]])

# Scale numeric features
scaler = StandardScaler()
X_num = scaler.fit_transform(df[["age"]])

# Combine features
X = np.hstack([X_text, X_cat.toarray(), X_num])
le = LabelEncoder()
y = le.fit_transform(df["job"])  # now y is integers [0..N-1]

# -------------------------------
# Train/Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Model Training
# -------------------------------
clf = XGBClassifier(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="mlogloss"
)
clf.fit(X_train, y_train)

# -------------------------------
# Evaluation - Top-3 Accuracy
# -------------------------------
probs = clf.predict_proba(X_test)
top3_preds = np.argsort(probs, axis=1)[:, -3:]
correct_top3 = sum(
    le.inverse_transform([y_test[i]])[0] in le.inverse_transform(top3_preds[i])
    for i in range(len(y_test))
)
top3_accuracy = correct_top3 / len(y_test)
print(f"Top-3 Accuracy: {top3_accuracy:.2%}")

# -------------------------------
# Example New User
# -------------------------------
new_user = pd.DataFrame([{
    "name": "Ana García",
    "age": 23,
    "user_city": "Madrid",
    "has_car": False,
    "education_level": "Bachelor",
    "english": True,
    "studies": "Business Administration",
    "company": "InnovaCorp",
    "job_city": "Madrid",
    "salary_range": "€1100-1300",
    "contract_type": "Internship"
}])

# Transform
new_X_text = embedder.encode(new_user["studies"], convert_to_numpy=True)
new_X_cat = ohe.transform(new_user[[
    "education_level", "english", "user_city", "job_city", "has_car", "contract_type"
]])
new_X_num = scaler.transform(new_user[["age"]])

new_X = np.hstack([new_X_text, new_X_cat.toarray(), new_X_num])

# Predict Top-3
new_probs = clf.predict_proba(new_X)[0]
top3_idx = np.argsort(new_probs)[-3:][::-1]
top3_jobs = le.inverse_transform(top3_idx)
top3_scores = new_probs[top3_idx]

print(f"\nTop-3 job recommendations for {new_user['name'][0]}:")
for job, score in zip(top3_jobs, top3_scores):
    print(f"  {job} -> {score:.2%}")

# Save model + encoders + scaler + label encoder
joblib.dump(clf, "primer-empleo/Model/xgb_model.pkl")
joblib.dump(ohe, "primer-empleo/Model/encoder.pkl")
joblib.dump(scaler, "primer-empleo/Model/scaler.pkl")
joblib.dump(le, "primer-empleo/Model/label_encoder.pkl")
