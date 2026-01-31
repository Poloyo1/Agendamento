import os
from dotenv import load_dotenv

load_dotenv()

INSTANCE_ID = os.getenv("INSTANCE_ID")
TOKEN = os.getenv("TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

GOOGLE_CREDENTIALS_FILE = "credentials.json"
TIMEZONE = "America/Sao_Paulo"
WHATSAPP_MODE = "fake"