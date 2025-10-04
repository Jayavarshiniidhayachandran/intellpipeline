import os
import pandas as pd
from github import Github, Auth

# -------------------------------
# 1️⃣ Read GitHub token from environment
# -------------------------------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment variables!")

# -------------------------------
# 2️⃣ Authenticate properly
# -------------------------------
auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)

# -------------------------------
# 3️⃣ Specify your repository
# Replace 'YourUsername/intellipipe' with your GitHub username and repo name
# -------------------------------
REPO_NAME = "Jayavarshiniidhayachandran/intellpipeline"  # <-- CHANGE THIS
repo = g.get_repo(REPO_NAME)

# -------------------------------
# 4️⃣ Collect workflow runs
# -------------------------------
workflow_runs = repo.get_workflow_runs()  # gets all workflow runs

# -------------------------------
# 5️⃣ Prepare CSV data
# -------------------------------
data = []
for run in workflow_runs:
    status = 1 if run.conclusion == "success" else 0
    commit_msg = run.head_commit.message if run.head_commit else ""

    # Count number of changed files safely
    num_changed_files = 0
    if run.head_commit:
        commit = run.head_commit
        try:
            files = commit.files if hasattr(commit, "files") else []
            num_changed_files = len(files)
        except Exception:
            num_changed_files = 0

    # Count error keywords in commit message
    keyword_count = sum(commit_msg.lower().count(k) for k in ["error", "fail", "exception"])
    
    # Placeholder for previous build status (can be improved later)
    prev_status = 1

    data.append([len(commit_msg), num_changed_files, keyword_count, prev_status, status])

# -------------------------------
# 6️⃣ Save CSV
# -------------------------------
df = pd.DataFrame(data, columns=["commit_msg_length", "num_changed_files", "keyword_count", "prev_status", "build_status"])

# Safe creation of data folder
if os.path.exists("data") and not os.path.isdir("data"):
    os.remove("data")  # remove file if exists
os.makedirs("data", exist_ok=True)

df.to_csv("data/build_data.csv", index=False)
print("✅ Build logs processed and saved to data/build_data.csv")


# scripts/process_logs.py
import os
import pandas as pd

# Create data folder
os.makedirs("data", exist_ok=True)

# Example: generate fake build logs data
data = {
    "commit_msg_length": [50, 10, 80],
    "num_changed_files": [3, 1, 5],
    "keyword_count": [1, 0, 2],
    "prev_status": [1, 0, 1],
    "build_status": [1, 0, 1]  # 1 = success, 0 = fail
}

df = pd.DataFrame(data)

# Save CSV
df.to_csv("data/build_data.csv", index=False)
print("✅ Build logs processed and saved to data/build_data.csv")

