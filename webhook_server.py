import os
import subprocess
from flask import Flask, request, jsonify
from threading import Thread

from config import GITHUB_REPO_URL, NOTEBOOK_PATH
from notebook_utils import summarize_notebook
from confluence_utils import update_confluence

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    def process_payload():
        try:
            print("📬 GitHub webhook received!")

            # Pull the repo (clone or pull)
            repo_name = GITHUB_REPO_URL.split('/')[-1].replace('.git', '')
            if not os.path.exists(repo_name):
                print(f"🔄 Cloning repo: {GITHUB_REPO_URL}")
                subprocess.run(["git", "clone", GITHUB_REPO_URL])
            else:
                print(f"🔁 Pulling latest changes in: {repo_name}")
                subprocess.run(["git", "-C", repo_name, "pull"])

            # Full path to notebook
            full_notebook_path = os.path.join(repo_name, NOTEBOOK_PATH)

            # Summarize notebook
            print(f"🧠 Summarizing notebook: {full_notebook_path}")
            summary = summarize_notebook(full_notebook_path)

            # Update Confluence
            print("📤 Updating Confluence page...")
            update_confluence(summary)

            print("✅ Workflow complete: summary posted to Confluence.")

        except Exception as e:
            print(f"❌ Error during webhook processing: {str(e)}")

    # Start the work in a background thread
    Thread(target=process_payload).start()

    # Respond immediately to GitHub to avoid webhook timeout
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
