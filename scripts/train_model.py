# scripts/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load the CSV
df = pd.read_csv("data/build_data.csv")

# Features and target
X = df[["commit_msg_length", "num_changed_files", "keyword_count", "prev_status"]]
y = df["build_status"]

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)
print("✅ Model trained")

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(clf, "models/model.pkl")
print("✅ Model saved as models/model.pkl")
