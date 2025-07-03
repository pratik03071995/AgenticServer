# from config import *

# print("GitHub:", GITHUB_REPO_URL)
# print("Notebook:", NOTEBOOK_PATH)
# print("Confluence Email:", CONFLUENCE_EMAIL)
# print("Confluence Token Present:", bool(CONFLUENCE_API_TOKEN))
# print("OpenAI Key Present:", bool(OPENAI_API_KEY))
# test_notebook_utils.py
from notebook_utils import summarize_notebook

summary = summarize_notebook("AgenticPOC/Simple_calculator.ipynb")
print(summary)

