
# 🧠 Agentic AI Notebook Auto-Documentation System

This project is a fully automated system that listens for notebook changes in a GitHub repository and pushes AI-generated summaries to Confluence — and now also sends an email notification after a successful update!

---

## 🚀 Overview

- **Trigger**: GitHub push to `AgenticPOC` repo
- **Automation Host**: Flask server running in `AgenticServer` repo
- **Processing**:
  - Pulls updated notebooks locally
  - Summarizes code with DeepSeek LLM
  - Converts to clean HTML with headings, bullet points, and icons
  - Pushes the output to Confluence via REST API
  - 📧 Sends an email notification with the Confluence page link

---

## 📁 Repositories

- `AgenticPOC`: Contains your Jupyter/Databricks notebooks
- `AgenticServer`: Contains the Flask app that receives webhook events, summarizes notebooks, and updates Confluence + sends emails

---

## 🔁 How It Works (Flow)

1. **Push to GitHub**  
   You push a `.ipynb` file to `AgenticPOC/main`.

2. **GitHub Webhook Fires**  
   GitHub sends a webhook to your Flask server in `AgenticServer`.

3. **Webhook Received**  
   The Flask server (`webhook_server.py`) receives the payload:
   - Parses modified/added files
   - Pulls the latest `AgenticPOC` repo locally
   - Identifies changed notebooks

4. **Notebook Summarization**  
   - Each changed notebook is loaded from disk
   - The source code is extracted and passed to DeepSeek API
   - AI returns a structured summary with markdown formatting

5. **HTML Conversion & Styling**  
   - Markdown is converted to valid Confluence-compatible HTML
   - Icons, headers, lists, and tip/info blocks are added
   - GitHub commit URL is appended at the bottom

6. **Push to Confluence**  
   - Confluence REST API is used to create or update a page in the desired space

7. **📧 Email Notification**  
   - After a successful Confluence update, an email is sent with the notebook name and direct Confluence page link.

---

## 🧱 Components

### 📂 `webhook_server.py`
- Flask app
- Handles GitHub POST webhook
- Pulls latest repo changes
- Routes notebooks to summarizer and formatter

### 📂 `notebook_utils.py`
- Loads `.ipynb` files
- Extracts code cells
- Sends prompt to DeepSeek LLM
- Returns structured markdown summary

### 📂 `confluence_utils.py`
- Converts markdown summary to Confluence HTML
- Adds icons, TOC, info/tip blocks
- Uses Confluence REST API to create/update a page
- **Sends email** after update

---

## ✅ Features

- 🔗 GitHub Commit traceability
- 📑 Confluence formatting: TOC, emojis, tip/info macros
- 💬 Clean AI summaries using LLM
- 📧 Email notifications after update
- 🚫 File-not-found safety check
- 🔄 Auto syncs local repo with GitHub pushes

---

## 🛠️ Setup Instructions

### 1. Clone `AgenticServer` repo

### 2. Create `.env` file with:

```env
GITHUB_REPO_URL=https://github.com/yourusername/AgenticPOC.git
CONFLUENCE_EMAIL=your_email@example.com
CONFLUENCE_API_TOKEN=base64_encoded_auth
CONFLUENCE_BASE_URL=https://yourcompany.atlassian.net/wiki
CONFLUENCE_SPACE_KEY=ABC

OPENAI_API_KEY=...
DEEPSEEK_API_KEY=...

# Email SMTP configuration
EMAIL_SENDER=you@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=you@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

> ✅ Use [Gmail App Passwords](https://support.google.com/accounts/answer/185833) instead of your regular Gmail password

### 3. Clone `AgenticPOC` repo into same directory:
```bash
git clone https://github.com/yourusername/AgenticPOC.git
```

### 4. Start Flask app:
```bash
python3 webhook_server.py
```

### 5. Configure GitHub webhook:
- Payload URL: `http://localhost:5050/webhook`
- Content type: `application/json`
- Events: `Just the push event`

---

## 📬 Output: Email Preview

**Subject:** `📄 Notebook Summary Published: guess_the_word`  
**Body:**
```
✅ The notebook *guess_the_word* has been summarized and published to Confluence.

🔗 View it here: https://pratik03071995.atlassian.net/wiki/spaces/NBDOCS/overview?atl_f=PAGETREE
```

---

## 📘 Contact

Maintainer: **Pratik**  
Email: pratik03071995@gmail.com  
Client: **Personal**

---

