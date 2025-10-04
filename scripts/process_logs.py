import os
import pandas as pd
from github import Github, Auth

# -------------------------------
# 1️⃣ Read GitHub token from environment
# -------------------------------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# -------------------------------
# 2️⃣ Authenticate properly
# -------------------------------
auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)

# -------------------------------
# 3️⃣ Specify your repository
# Replace 'your-username/intellipipe' with your GitHub username and repo name
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
    num_changed_files = len(run.head_commit.modified) if run.head_commit else 0
    keyword_count = sum(commit_msg.lower().count(k) for k in ["error", "fail", "exception"])
    prev_status = 1  # you can improve later
    data.append([len(commit_msg), num_changed_files, keyword_count, prev_status, status])

# -------------------------------
# 6️⃣ Save CSV
# -------------------------------
df = pd.DataFrame(data, columns=["commit_msg_length", "num_changed_files", "keyword_count", "prev_status", "build_status"])
os.makedirs("data", exist_ok=True)
df.to_csv("data/build_data.csv", index=False)
print("✅ Build logs processed and saved to data/build_data.csv")

