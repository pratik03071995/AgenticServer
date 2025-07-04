
# 🧠 Agentic AI Notebook Auto-Documentation System

This project listens for Jupyter/Databricks notebook updates in GitHub and automatically summarizes them using AI, updates a Confluence page, and sends an email notification.

---

## 🚀 Overview

- **Trigger**: GitHub push to `AgenticPOC` repo
- **Automation Host**: Flask server in `AgenticServer` repo
- **Flow**:
  - Pulls updated notebooks
  - Summarizes using DeepSeek LLM
  - Converts to formatted HTML
  - Pushes to Confluence
  - Sends email notification
  - Uses `ngrok` for webhook testing if needed

---

## 📁 Repositories

- `AgenticPOC`: Notebook repository
- `AgenticServer`: Flask automation server (this project)

---

## 🔁 How It Works

1. GitHub push triggers webhook
2. Flask receives push payload
3. Notebook code is summarized via LLM
4. HTML is generated with clean formatting
5. Page is updated or created in Confluence
6. Email notification is sent
7. Git commit link included

---

## 🛠️ Setup Instructions

### 1. Clone Both Repositories

```bash
git clone https://github.com/yourusername/AgenticServer.git
cd AgenticServer
git clone https://github.com/yourusername/AgenticPOC.git
```

---

### 2. Create a `.env` File

Inside `AgenticServer/`, create a `.env` file:

```env
# Git
GITHUB_REPO_URL=https://github.com/yourusername/AgenticPOC.git

# Confluence
CONFLUENCE_EMAIL=you@example.com
CONFLUENCE_API_TOKEN=base64_encoded_auth
CONFLUENCE_BASE_URL=https://yourcompany.atlassian.net/wiki
CONFLUENCE_SPACE_KEY=ABC

# AI keys
OPENAI_API_KEY=...
DEEPSEEK_API_KEY=...

# Email
EMAIL_SENDER=you@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=you@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Start Flask Server

```bash
python3 webhook_server.py
```

This starts the listener on `http://localhost:5050/webhook`

---

### 5. Expose Flask Server with ngrok (For GitHub Webhook)

#### ⬇️ Install ngrok:
```bash
brew install --cask ngrok  # macOS
# or download manually from https://ngrok.com/download
```

#### 🔐 Set auth token (once):
```bash
ngrok config add-authtoken <your_ngrok_token>
```

#### 🚀 Start tunnel:
```bash
ngrok http 5050
```

This gives you a public URL like:
```
https://abc123.ngrok.io → http://localhost:5050
```

---

### 6. Configure GitHub Webhook

- Go to your GitHub repo (`AgenticPOC`)
- Settings → Webhooks → Add webhook
- **Payload URL**: `https://abc123.ngrok.io/webhook`
- **Content type**: `application/json`
- **Trigger**: Just the push event
- Save ✅

---

## 📬 Output

### ✅ Email

You’ll receive:
```
Subject: 📄 Notebook Summary Published: guess_the_word
Body:
✅ The notebook *guess_the_word* has been summarized and published to Confluence.
🔗 View it here: [confluence link]
```

---

## 💡 Tips

- If you use Gmail, enable **App Passwords**
- Confluence pages will show Git commit links for traceability
- Format includes TOC, emojis, structured lists

---

## 📘 Maintainer

**Pratik**   
📫 pratik03071995@gmail.com

---
