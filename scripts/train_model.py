
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load dataset
df = pd.read_csv("data/build_data.csv")

X = df[["commit_msg_length", "num_changed_files", "keyword_count", "prev_status"]]
y = df["build_status"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
print(f"✅ Model trained. Accuracy: {clf.score(X_test, y_test)*100:.2f}%")

# Save model
os.makedirs("models", exist_ok=True)           # Create folder if not exists
joblib.dump(clf, "models/model.pkl")          # Save model
print("✅ Model saved as models/model.pkl")
