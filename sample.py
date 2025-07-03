# === Full End-to-End Integration: GitHub -> Notebook Summary -> Confluence ===

import os
import json
import subprocess
import openai
import requests
from flask import Flask, request, jsonify
from requests.auth import HTTPBasicAuth

# === Configuration ===
NOTEBOOK_PATH = "Simple_calculator.ipynb"  # Path to your local notebook after pull
GITHUB_REPO_URL = "https://github.com/pratik03071995/AgenticPOC.git"
CONFLUENCE_PAGE_ID = "131073"  # replace with your real page ID
CONFLUENCE_BASE_URL = "https://pratik03071995.atlassian.net/wiki"
CONFLUENCE_EMAIL = "your_email@example.com"
CONFLUENCE_API_TOKEN = "your_confluence_api_token"

openai.api_key = os.environ.get("OPENAI_API_KEY")  # Store this securely!

# === Flask App ===
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        print("📩 Webhook triggered by GitHub push event!")

        # Pull the latest notebook
        if not os.path.exists("AgenticPOC"):
            subprocess.run(["git", "clone", GITHUB_REPO_URL])
        else:
            subprocess.run(["git", "-C", "AgenticPOC", "pull"])

        notebook_path = os.path.join("AgenticPOC", NOTEBOOK_PATH)

        # Summarize notebook
        summary = summarize_notebook(notebook_path)
        print("🧠 Summary generated. Posting to Confluence...")

        # Update Confluence
        update_confluence_page(summary)
        print("✅ Confluence page updated.")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# === Notebook Summarizer ===
def summarize_notebook(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    code_cells = [cell['source'] for cell in nb['cells'] if cell['cell_type'] == 'code']
    code_text = "\n".join(["".join(c) for c in code_cells])

    prompt = f"""
You are an AI code summarizer. Please explain the purpose and logic of this Databricks notebook in a clear and concise way:

{code_text[:6000]}  # truncate for token safety
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response['choices'][0]['message']['content']


# === Confluence Page Updater ===
def update_confluence_page(summary_text):
    # 1. Get current version and page info
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{CONFLUENCE_PAGE_ID}?expand=body.storage,version"
    res = requests.get(url, auth=HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN))
    page = res.json()

    current_version = page['version']['number']
    title = page['title']

    new_body = f"<p>📝 Latest summary (auto-updated):</p><pre>{summary_text}</pre>"

    update_payload = {
        "version": {"number": current_version + 1},
        "title": title,
        "type": "page",
        "body": {
            "storage": {
                "value": new_body,
                "representation": "storage"
            }
        }
    }

    update_url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{CONFLUENCE_PAGE_ID}"
    update_res = requests.put(update_url, json=update_payload,
                              auth=HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN))
    if update_res.status_code != 200:
        raise Exception(f"Failed to update Confluence: {update_res.status_code} - {update_res.text}")


# === Run the Flask server ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
