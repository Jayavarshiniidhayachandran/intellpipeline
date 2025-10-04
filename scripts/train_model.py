import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# -------------------------------
# 1️⃣ Load the dataset
# -------------------------------
data_path = "data/build_data.csv"
if not os.path.exists(data_path):
    raise FileNotFoundError(f"{data_path} not found! Make sure process_logs.py ran successfully.")

df = pd.read_csv(data_path)

# Features and target
X = df[["commit_msg_length", "num_changed_files", "keyword_count", "prev_status"]]
y = df["build_status"]

# -------------------------------
# 2️⃣ Split into train/test
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------------
# 3️⃣ Train classifier
# -------------------------------
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# -------------------------------
# 4️⃣ Evaluate accuracy (optional)
# -------------------------------
accuracy = clf.score(X_test, y_test)
print(f"✅ Model trained! Accuracy on test set: {accuracy*100:.2f}%")

# -------------------------------
# 5️⃣ Save model
# -------------------------------
os.makedirs("models", exist_ok=True)            # create folder if it doesn't exist
joblib.dump(clf, "models/model.pkl")           # save model
print("✅ Model saved as models/model.pkl")
