import requests

BASE_URL = "http://localhost:8000"  # change if needed


def chat(user_input: str, messages: list):
    """Call normal chat endpoint."""
    payload = {"prompt": user_input, "history": messages}
    print(payload)
    response = requests.post(f"{BASE_URL}/api/chat", json=payload)
    response.raise_for_status()
    print(response.json())
    return response.json().get("answer", "No response from API")


def file_chat(user_input: str, messages: list):
    """Call file-aware chat endpoint."""
    payload = {"prompt": user_input, "history": messages}
    response = requests.post(f"{BASE_URL}/api/file-chat", json=payload)
    response.raise_for_status()
    print(response.json())
    return response.json().get("answer", "No response from API")


def upload_pdf(file):
    """Upload file to backend API."""
    files = {"file": (file.name, file.getvalue(), "application/pdf")}
    response = requests.post(f"{BASE_URL}/api/upload-pdf/", files=files)
    response.raise_for_status()
    return response.json()

def get_stock_info(query: str):
    """Fetch stock information from backend API."""
    response = requests.post(f"{BASE_URL}/api/mcp/planner?req={query}")
    response.raise_for_status()
    print(response.json())
    return response.json().get("answer", "No response from API")