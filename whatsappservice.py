import requests
import json
import sys

def SendMessageWhatsapp(data):
    try:
        token = "EAAK2hRpoqgYBP9orK3Lq1LDhawzuuOpMoyulWL3a5e8Iy1glqv7JjbPOdrqyofhYXz9ZCauPMccYdfTqD4nohEdkZBE7YIZBAFv9nfehgFwCNAy83yZBY9o8W3SLrGFISAClqvDZAvaveM7qag9Rk9mUeJgjFnEvSnfZBn9Fx41AjpXsOlXw5CdIzNlUBbIVfsRAZDZD"
        api_url = "https://graph.facebook.com/v22.0/878228345368187/messages"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }

        print(">>> Llamando a Meta:", api_url, file=sys.stdout, flush=True)
        print(">>> Payload:", json.dumps(data), file=sys.stdout, flush=True)

        response = requests.post(api_url, data=json.dumps(data), headers=headers)

        print(">>> Respuesta Meta status:", response.status_code, file=sys.stdout, flush=True)
        print(">>> Respuesta Meta body:", response.text, file=sys.stdout, flush=True)

        if response.status_code == 200:
            return True

        return False

    except Exception as exception:
        print(">>> ERROR SendMessageWhatsapp:", repr(exception), file=sys.stderr, flush=True)
        return False
