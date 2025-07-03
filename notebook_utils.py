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

        # Build the prompt
        prompt = f"""
You are an AI summarizer. Please summarize the purpose and logic of this Databricks or Jupyter notebook in a clear and concise way for a technical Confluence audience:

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
