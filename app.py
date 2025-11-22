import os
from flask import Flask, request, jsonify
import sys
import util
import whatsappservice
from collections import deque   #para evitar mensajes duplicados que envíe el bot solo

# Guardamos los últimos N IDs de mensajes procesados para evitar duplicados
PROCESSED_MESSAGE_IDS = deque(maxlen=100)

contact_number = "+1234567890"

app = Flask(__name__)
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "320r7th34pg8y34hf9834f7934")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/welcome', methods=['GET'])
def index():
    return "Hello, developer\n"

@app.route("/version", methods=["GET"])
def version():
    return "VERSION-PROCESS-ONLY-1", 200

@app.route('/whatsapp', methods=['GET'])
def VerifyToken():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        # Pequeño log de depuración
        print(">>> GET /whatsapp:", token, challenge, file=sys.stdout, flush=True)

        if token is not None and challenge is not None and token == VERIFY_TOKEN:
            return challenge
        else:
            return "", 400
    except Exception as e:
        print(">>> ERROR VerifyToken:", repr(e), file=sys.stderr, flush=True)
        return "", 400

@app.route('/whatsapp', methods=['POST'])
def RecivedMessage():
    try:
        body = request.get_json(silent=True) or {}
        print("WEBHOOK BODY:", body, flush=True)
        print(">>> POST /whatsapp BODY:", body, file=sys.stdout, flush=True)

        # A veces Meta manda eventos sin 'messages' (por ejemplo, statuses)
        entries = body.get("entry") or []
        if not entries:
            print(">>> Webhook sin 'entry'. Nada que procesar.", file=sys.stdout, flush=True)
            return "EVENT_RECEIVED"

        changes = entries[0].get("changes") or []
        if not changes:
            print(">>> Webhook sin 'changes'. Nada que procesar.", file=sys.stdout, flush=True)
            return "EVENT_RECEIVED"

        value = changes[0].get("value") or {}

        messages = value.get("messages")
        if not messages:
            print(">>> Webhook sin 'messages' (probablemente status). Nada que responder.", file=sys.stdout, flush=True)
            return "EVENT_RECEIVED"

        message = messages[0]
        number = message.get("from")
        if not number:
            print(">>> Mensaje sin número 'from'.", file=sys.stdout, flush=True)
            return "EVENT_RECEIVED"

        # --- EVITAR DUPLICADOS: si ya procesamos este ID, no respondemos otra vez ---
        msg_id = message.get("id")
        if msg_id:
            if msg_id in PROCESSED_MESSAGE_IDS:
                print(">>> Mensaje duplicado, se ignora:", msg_id, file=sys.stdout, flush=True)
                return "EVENT_RECEIVED"
            PROCESSED_MESSAGE_IDS.append(msg_id)

        # --- PROCESAR SOLO MENSAJES DE TEXTO ---
        #msg_type = message.get("type")
        #if msg_type != "text":
        #    print(">>> Mensaje no es de tipo 'text' (es:", msg_type, "), se ignora.", file=sys.stdout, flush=True)
        #    return "EVENT_RECEIVED"


        text = util.GetTextUser(message)

        # Fallback por si util.GetTextUser no devuelve nada en mensajes de texto normales
        if not text:
            raw_text = (message.get("text") or {}).get("body")
            if raw_text:
                text = raw_text
                
        print(f">>> Mensaje recibido de {number}: {text}", file=sys.stdout, flush=True)

        ProcessMessages(text, number)

        return "EVENT_RECEIVED"
    except Exception as e:
        print(">>> ERROR RecivedMessage:", repr(e), file=sys.stderr, flush=True)
        return "EVENT_RECEIVED"

def ProcessMessages(text, number):
    # Normaliza para comparar sin problemas de mayúsculas/acentos básicos
    normalized = (text or "").strip().lower()
    listData = []

    if any(word in normalized for word in ["hola", "hi", "hello", "buenas", "opcion", "opción"]):
        data = util.TextMessage("¡Hola! ¿En qué puedo ayudarte hoy?", number)
        dataMenu = util.ListMessage(number)
        
        listData.append(data)
        listData.append(dataMenu)        
    elif "gracias" in normalized:
        data = util.TextMessage("¡Gracias a ti! Nos vemos pronto.", number)
        listData.append(data)
    elif "agency" in normalized:
        data = util.TextMessage("Esta es nuestro equipo de la empresa", number)
        dataLocation = util.LocationMessage(number)
        listData.append(data)
        listData.append(dataLocation)
    elif "contact" in normalized:
        data = util.TextMessage(f"*Puedes contactarnos en:*\n{contact_number}", number)
        listData.append(data)

    elif "buy" in normalized:
        data = util.ButtonsMessage(number)
        listData.append(data)

    elif "sell" in normalized:
        data = util.ButtonsMessage(number)
        listData.append(data)

    elif "sí" in normalized:
        data = util.TextMessage("Entra en este link para registrarte: URL", number)
        listData.append(data)

    elif "no" in normalized:
        data = util.TextMessage("Entra en este link para iniciar sesión: URL", number)
        listData.append(data)

    else:
        data = util.TextMessage("Lo siento, no pude entenderte. ¿Puedes intentarlo de otra manera?", number)
        listData.append(data)

    for item in listData:
        whatsappservice.SendMessageWhatsapp(item)

def GenerateMessage(text, number):
    # Normalizamos por si acaso
    text = text.lower()

    data = None

    if "text" in text:
        data = util.TextMessage("text", number)

    if "format" in text:
        data = util.TextFormatMessage(number)

    if "image" in text:
        data = util.ImageMessage(number)

    if "audio" in text:
        data = util.AudioMessage(number)

    if "video" in text:
        data = util.VideoMessage(number)

    if "document" in text:
        data = util.DocumentMessage(number)

    if "location" in text:
        data = util.LocationMessage(number)

    if "button" in text:
        data = util.ButtonsMessage(number)

    if "list" in text:
        data = util.ListMessage(number)

    # Fallback si no coincide ninguna palabra clave
    if data is None:
        data = util.TextMessage(f"Recibí tu mensaje: {text}", number)

    print(">>> Enviando respuesta a WhatsApp:", data, file=sys.stdout, flush=True)
    whatsappservice.SendMessageWhatsapp(data)

if __name__ == '__main__':
    app.run()
