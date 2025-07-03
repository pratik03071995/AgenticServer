import requests
from requests.auth import HTTPBasicAuth
import markdown
from config import *

def update_confluence(summary_text):
    # 1. Get current page content
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{CONFLUENCE_PAGE_ID}?expand=body.storage,version"
    res = requests.get(url, auth=HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN))
    if res.status_code != 200:
        raise Exception(f"Error fetching Confluence page: {res.text}")
    page = res.json()

    current_version = page["version"]["number"]
    title = page["title"]

    # Convert Markdown to HTML
    html_summary = markdown.markdown(summary_text)

    # Wrap in clean Confluence-compatible div
    new_body = f"""
    <p>📝 <b>Latest summary (auto-updated):</b></p>
    <div>{html_summary}</div>
    """


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
