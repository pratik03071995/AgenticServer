from flask import Flask, request, jsonify
from threading import Thread
import os, subprocess, json

from config import GITHUB_REPO_URL
from notebook_utils import summarize_notebook
from confluence_utils import create_or_update_page

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.json

    def process_payload():
        try:
            print("📬 GitHub webhook received!")

            repo_name = GITHUB_REPO_URL.split('/')[-1].replace('.git', '')
            if not os.path.exists(repo_name):
                subprocess.run(["git", "clone", GITHUB_REPO_URL])
            else:
                subprocess.run(["git", "-C", repo_name, "pull"])

            # ✅ Loop through each commit in the push payload
            for commit in payload.get("commits", []):
                commit_url = commit.get("url")  # 🔗 GitHub commit URL
                changed_files = commit.get("modified", []) + commit.get("added", [])

                for file in changed_files:
                    if file.endswith(".ipynb"):
                        full_path = os.path.join(repo_name, file)
                        print(f"🧠 Summarizing: {full_path}")
                        summary = summarize_notebook(full_path)

                        notebook_name = os.path.splitext(os.path.basename(file))[0]
                        print(f"📄 Updating Confluence page: {notebook_name}")
                        create_or_update_page(notebook_name, summary, commit_url)

            print("✅ All notebook pages updated.")

        except Exception as e:
            print(f"❌ Error: {e}")

    Thread(target=process_payload).start()
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
