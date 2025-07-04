
# 🧠 Agentic AI Notebook Auto-Documentation System

This project is a fully automated system that listens for notebook changes in a GitHub repository and pushes AI-generated summaries to Confluence in real time.

---

## 🚀 Overview

- **Trigger**: GitHub push to `AgenticPOC` repo
- **Automation Host**: Flask server running in `AgenticServer` repo
- **Processing**:
  - Pulls updated notebooks locally
  - Summarizes code with DeepSeek LLM
  - Converts to clean HTML with headings, bullet points, and icons
  - Pushes the output to Confluence via REST API

---

## 📁 Repositories

- `AgenticPOC`: Contains your Jupyter/Databricks notebooks
- `AgenticServer`: Contains the Flask app that receives webhook events, summarizes notebooks, and updates Confluence

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
   - Summary is published for team visibility with styling and traceability

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
- Uses Confluence REST API to create or update a page

---

## ✅ Features

- 🔗 GitHub Commit traceability
- 📑 Confluence formatting: TOC, emojis, tip/info macros
- 💬 Clean AI summaries using LLM
- 🚫 File-not-found safety check
- 🔄 Auto syncs local repo with GitHub pushes

---

## 🛠️ Setup Instructions

1. Clone `AgenticServer` repo
2. Create `.env` file with keys:
   ```env
   GITHUB_REPO_URL=https://github.com/yourusername/AgenticPOC.git
   CONFLUENCE_EMAIL=your_email@example.com
   CONFLUENCE_API_TOKEN=base64_encoded_auth
   CONFLUENCE_BASE_URL=https://yourcompany.atlassian.net/wiki
   CONFLUENCE_SPACE_KEY=ABC
   OPENAI_API_KEY=...
   DEEPSEEK_API_KEY=...
   ```

3. Clone `AgenticPOC` repo into the same directory as `webhook_server.py`:
   ```bash
   git clone https://github.com/yourusername/AgenticPOC.git
   ```

4. Start your Flask app:
   ```bash
   python3 webhook_server.py
   ```

5. Configure GitHub webhook:
   - Payload URL: `http://yourserver:5050/webhook`
   - Content type: `application/json`
   - Events: `Just the push event`

---

## 📦 Output Example in Confluence

```markdown
🎯 Purpose
- Explain what the notebook does

🔍 Key Logic & Steps
1. Load data from file
2. Preprocess and clean
3. Model training or visualization

📘 Technical Audience Notes
- Uses pandas, matplotlib, sklearn
- JSON/CSV I/O

📌 Use Case
- Reproducible financial forecasting pipeline

🔗 GitHub Commit: [view commit](https://github.com/your-repo/commit/abc123)
```

---

## 📬 Contact

Maintainer: **Pratik**  
Email: pratik03071995@gmail.com.com  
Client: **Personal**

---

