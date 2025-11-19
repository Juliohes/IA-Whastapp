from flask import Flask, request, jsonify
import sys 
import util
import whatsappservice

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/welcome', methods=['GET'])
def index():
    return "Hello, developer\n"

@app.route('/whatsapp', methods=['GET'])
def VerifyToken():
    try:
        access_token = "320r7th34pg8y34hf9834f7934"
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        # Pequeño log de depuración
        print(">>> GET /whatsapp:", token, challenge, file=sys.stdout, flush=True)

        if token is not None and challenge is not None and token == access_token:
            return challenge
        else:
            return "", 400
    except Exception as e:
        print(">>> ERROR VerifyToken:", repr(e), file=sys.stderr, flush=True)
        return "", 400

@app.route('/whatsapp', methods=['POST'])
def RecivedMessage():
    try:
        body = request.get_json()
        print("WEBHOOK BODY:", body, flush=True)
        print(">>> POST /whatsapp BODY:", body, file=sys.stdout, flush=True)

        # A veces Meta manda eventos sin 'messages' (por ejemplo, statuses)
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        messages = value.get("messages")
        if not messages:
            print(">>> Webhook sin 'messages' (probablemente status). Nada que responder.", file=sys.stdout, flush=True)
            return "EVENT_RECEIVED"

        message = messages[0]
        number = message["from"]

        text = util.GetTextUser(message)
        print(f">>> Mensaje recibido de {number}: {text}", file=sys.stdout, flush=True)

        ProcessMessages(text, number)

        return "EVENT_RECEIVED"
    except Exception as e:
        print(">>> ERROR RecivedMessage:", repr(e), file=sys.stderr, flush=True)
        return "EVENT_RECEIVED"

def ProcessMessages(text, number):
    text = text.lower()
    
    if "hola" in text or "hi" in text or "hello" in text or "Buenas" in text:
        data = util.TextMessage("¡Hola! ¿En qué puedo ayudarte hoy?", number)
    elif "Gracias" in text:
        data = util.TextMessage("¡Gracias a tí. Nos vemos pronto.", number)
    else:
        data = util.TextMessage(f"Lo siento, no puedo entenderte", number)
        
    whatsappservice.SendMessageWhatsapp(data)

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
