import os
import pandas as pd
from github import Github

# ------------------------------
# CONFIGURATION
# ------------------------------
GITHUB_TOKEN = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"  # replace with your token
REPO_NAME = "your-username/intellipipe"            # replace with your repo name

# ------------------------------
# CONNECT TO GITHUB
# ------------------------------
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# ------------------------------
# FETCH WORKFLOW RUNS
# ------------------------------
workflow_runs = repo.get_workflow_runs()  # fetch all workflow runs
data = []

for run in workflow_runs:
    status = 1 if run.conclusion == "success" else 0  # 1=success, 0=failure
    commit_msg = run.head_commit.message if run.head_commit else ""
    num_changed_files = len(run.head_commit.modified) if run.head_commit else 0

    # Check for error keywords in logs (simple placeholder)
    error_keywords = ["error", "exception", "failed"]
    log_text = ""  # placeholder, advanced: download actual logs later
    keyword_count = sum(1 for kw in error_keywords if kw in log_text.lower())

    # Previous build status (simplified placeholder)
    prev_status = 1  

    data.append({
        "commit_msg_length": len(commit_msg),
        "num_changed_files": num_changed_files,
        "keyword_count": keyword_count,
        "prev_status": prev_status,
        "build_status": status
    })

# ------------------------------
# SAVE CSV
# ------------------------------
os.makedirs("data", exist_ok=True)
df = pd.DataFrame(data)
df.to_csv("data/build_data.csv", index=False)
print("✅ Build logs processed and saved to data/build_data.csv")

