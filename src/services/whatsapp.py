import requests
from config import INSTANCE_ID, TOKEN, ZAPI_CLIENT_TOKEN, WHATSAPP_MODE

def send_message(phone, text):
    if WHATSAPP_MODE == "fake":
        print(f"\n📲 [WHATSAPP FAKE]")
        print(f"Para: {phone}")
        print(f"Mensagem: {text}\n")
        return True
    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{TOKEN}/send-text"
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN
    }

    payload = {
        "phone": phone,
        "message": text
    }

    requests.post(url, json=payload, headers=headers)
