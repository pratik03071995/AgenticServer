import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL")
NOTEBOOK_PATH = os.getenv("NOTEBOOK_PATH")  # e.g., Simple_calculator.ipynb

CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
CONFLUENCE_PAGE_ID = os.getenv("CONFLUENCE_PAGE_ID")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")


# ➕ Compatibility aliases
CONFLUENCE_USER = CONFLUENCE_EMAIL
CONFLUENCE_URL = CONFLUENCE_BASE_URL
SPACE_KEY = CONFLUENCE_SPACE_KEY

# 📧 Email notification config
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))  
