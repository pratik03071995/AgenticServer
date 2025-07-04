import requests
import json
import re
import smtplib
from email.mime.text import MIMEText
from config import (
    CONFLUENCE_API_TOKEN,
    CONFLUENCE_USER,
    CONFLUENCE_URL,
    SPACE_KEY,
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    EMAIL_RECEIVER,
    SMTP_SERVER,
    SMTP_PORT
)

headers = {
    "Authorization": f"Basic {CONFLUENCE_API_TOKEN}",
    "Content-Type": "application/json"
}

def send_email_notification(notebook_name, confluence_url):
    subject = f"📄 Confluence Update: {notebook_name}"
    body = f"""✅ The notebook *{notebook_name}* has been summarized and published to Confluence.

🔗 View it here: {confluence_url}
"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"📧 Email sent to {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def create_page(space, title, body, parent_id=None):
    print(f"[DEBUG] Creating page: '{title}' in space: '{space}' with parent_id: {parent_id}")
    url = f"{CONFLUENCE_URL}/rest/api/content/"
    data = {
        "type": "page",
        "title": title,
        "space": {"key": space},
        "body": {
            "storage": {
                "value": body,
                "representation": "storage"
            }
        },
        "ancestors": [{"id": parent_id}] if parent_id else []
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

def update_page(page_id, title, body, version):
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}"
    data = {
        "id": page_id,
        "type": "page",
        "title": title,
        "version": {"number": version + 1},
        "body": {
            "storage": {
                "value": body,
                "representation": "storage"
            }
        }
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    return response

def get_page_by_title(space, title):
    url = f"{CONFLUENCE_URL}/rest/api/content"
    params = {
        "title": title,
        "spaceKey": space,
        "expand": "version"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            return results[0]
    return None

def markdown_to_confluence_html(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(.+?)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text

def format_summary_as_html(summary: str) -> str:
    sections = re.split(r"\*\*(.+?):\*\*", summary)
    html_parts = []
    icons = {
        "Summary": "⚙️",
        "Purpose": "🎯",
        "Logic": "🔍",
        "Key Logic": "🔍",
        "Technical Audience Notes": "🧪",
        "Audience Note": "📘",
        "Use Case": "📌",
        "Key Takeaway": "💡"
    }

    for i in range(1, len(sections), 2):
        heading = sections[i].strip()
        content = sections[i + 1].strip() if i + 1 < len(sections) else ""
        icon = icons.get(heading, "📎")
        html_parts.append(f"<h2>{icon} {heading}</h2>")

        lines = content.strip().split('\n')
        list_items = [line.strip() for line in lines if line.strip().startswith(("1.", "2.", "3.", "-", "*"))]

        if list_items:
            if all(line.startswith(tuple(f"{n}." for n in range(1, 10))) for line in list_items):
                html_parts.append("<ol>")
                for line in list_items:
                    item = markdown_to_confluence_html(re.sub(r"^\d+\.\s*", "", line))
                    html_parts.append(f"<li>{item}</li>")
                html_parts.append("</ol>")
            else:
                html_parts.append("<ul>")
                for line in list_items:
                    item = markdown_to_confluence_html(re.sub(r"^[-*]\s*", "", line))
                    html_parts.append(f"<li>{item}</li>")
                html_parts.append("</ul>")
        elif heading == "Key Takeaway":
            html_parts.append(f"<ac:structured-macro ac:name='info'><ac:rich-text-body><p>{markdown_to_confluence_html(content)}</p></ac:rich-text-body></ac:structured-macro>")
        elif heading in ["Audience Note", "Technical Audience Notes"]:
            html_parts.append(f"<ac:structured-macro ac:name='tip'><ac:rich-text-body><p>{markdown_to_confluence_html(content)}</p></ac:rich-text-body></ac:structured-macro>")
        else:
            html_parts.append(f"<p>{markdown_to_confluence_html(content)}</p>")

    toc_html = "<ac:structured-macro ac:name='toc' />"
    if "Notebook Summary" not in summary:
        toc_html += "<h1>Notebook Summary</h1>\n"
    full_html = toc_html + "\n".join(html_parts)
    return full_html

def create_or_update_page(title, summary, commit_url=None):
    wrapped_body = format_summary_as_html(summary)
    if commit_url:
        wrapped_body += "<br /><br /><hr />\n"
        wrapped_body += f'<p><strong>GitHub Commit:</strong> <a href="{commit_url}" target="_blank">{commit_url}</a></p>'

    page = get_page_by_title(SPACE_KEY, title)
    if page:
        page_id = page["id"]
        version = page["version"]["number"]
        print(f"[INFO] Page '{title}' exists. Updating (ID: {page_id}, Version: {version})")
        response = update_page(page_id, title, wrapped_body, version)
    else:
        print(f"[INFO] Page '{title}' does not exist. Creating new page.")
        response = create_page(SPACE_KEY, title, wrapped_body)

    if response.status_code in [200, 201]:
        page_id = response.json().get("id", "unknown")
        page_url = f"{CONFLUENCE_URL}/pages/viewpage.action?pageId={page_id}"
        send_email_notification(title, page_url)
        print(f"[SUCCESS] Page '{title}' created/updated successfully.")
    else:
        print(f"[ERROR] Failed to update/create page: {response.status_code} - {response.text}")
