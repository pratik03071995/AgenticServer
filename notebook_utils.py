import json
import requests
from config import DEEPSEEK_API_KEY

def summarize_notebook(path):
    try:
        # Load notebook
        with open(path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        # Extract code cells
        code_cells = [
            cell['source']
            for cell in notebook.get('cells', [])
            if cell.get('cell_type') == 'code'
        ]

        code_text = "\n".join(["".join(c) for c in code_cells])[:6000]

        # Improved prompt to enforce structured, Confluence-friendly format
        prompt = f"""
You are an AI assistant that generates clean, Confluence-ready summaries for Jupyter or Databricks notebooks.

Structure the summary exactly like this:

**Purpose:**
- One sentence summary of the notebook’s goal

**Key Logic & Steps:**
1. Step description (no subheadings)
2. Step description
3. Step description

**Technical Audience Notes:**
- List key libraries and techniques used

**Use Case:**
- Where and how this notebook is useful

✅ Do NOT include subheadings like **Step Title**. Use only bullet or numbered lines.

Notebook content:
{code_text}
"""

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"DeepSeek API error {response.status_code}: {response.text}")

        summary = response.json()["choices"][0]["message"]["content"]
        return summary.strip()

    except Exception as e:
        raise Exception(f"Failed to summarize notebook using DeepSeek: {str(e)}")
