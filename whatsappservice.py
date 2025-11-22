import os
import requests
import json
import sys

API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v22.0")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID", "878228345368187")
TOKEN = os.getenv("WHATSAPP_TOKEN", "EAAK2hRpoqgYBP9orK3Lq1LDhawzuuOpMoyulWL3a5e8Iy1glqv7JjbPOdrqyofhYXz9ZCauPMccYdfTqD4nohEdkZBE7YIZBAFv9nfehgFwCNAy83yZBY9o8W3SLrGFISAClqvDZAvaveM7qag9Rk9mUeJgjFnEvSnfZBn9Fx41AjpXsOlXw5CdIzNlUBbIVfsRAZDZD")
API_URL = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"

def SendMessageWhatsapp(data):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}"
        }

        print(">>> Llamando a Meta:", API_URL, file=sys.stdout, flush=True)
        print(">>> Payload:", json.dumps(data), file=sys.stdout, flush=True)

        response = requests.post(API_URL, data=json.dumps(data), headers=headers)

        print(">>> Respuesta Meta status:", response.status_code, file=sys.stdout, flush=True)
        print(">>> Respuesta Meta body:", response.text, file=sys.stdout, flush=True)

        if response.status_code == 200:
            return True

        return False

    except Exception as exception:
        print(">>> ERROR SendMessageWhatsapp:", repr(exception), file=sys.stderr, flush=True)
        return False
