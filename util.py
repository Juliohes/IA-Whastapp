def GetTextUser(message):
    """
    Extrae el texto principal de un mensaje de WhatsApp (texto o interactivo).
    Devuelve string vacío si no hay contenido manejable.
    """
    if not message:
        return ""

    typeMessage = message.get("type")
    if typeMessage == "text":
        return (message.get("text") or {}).get("body", "")

    if typeMessage == "interactive":
        interactiveObject = message.get("interactive") or {}
        interactiveType = interactiveObject.get("type")

        if interactiveType == "button_reply":
            return (interactiveObject.get("button_reply") or {}).get("title", "")
        if interactiveType == "list_reply":
            return (interactiveObject.get("list_reply") or {}).get("title", "")

        print("Sin mensaje interactivo reconocido")
        return ""

    print("Sin mensaje manejable (tipo no soportado)")
    return ""

def TextMessage(text, number):
    data = {
                "messaging_product": "whatsapp",
                "to": number,
                "text": {
                    "body": text
                },
                "type": "text"
            }
    return data

def TextFormatMessage(number):
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "text",
            "text": {
                "body": "*Información importante*\n_Necesitas enviar tu correo_ \n-Pero tiene que estar-\n'''en dieferente formato'''"
            }
        }
    return data

def ImageMessage(number):
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "image",
            "image": {
                "link": "https://example.com/image.jpg"
            }
        }
    return data

def AudioMessage(number):
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "audio",
            "audio": {
                "link": "https://example.com/audio.mp3"
            }
        }
    return data

def VideoMessage(number):
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "video",
            "video": {
                "link": "https://example.com/video.mp4"
            }
        }
    return data

def DocumentMessage(number):
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "document",
            "document": {
                "link": "https://example.com/documet.pdf"
            }
        }
    return data

def LocationMessage(number):
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "location",
            "location": {
                "latitude": "38.87007",
                "longitude": "-6.98611",
                "name": "Home",
                "address": "Avenida José María Alcaraz y Alenda 14" 
            }
        }
    return data

def ButtonsMessage(number):
    data = {
            "messaging_product": "whatsapp",
            #"recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": "¿Confirmas tu registro?"
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "001",
                                "title": "Sí"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "002",
                                "title": "No"
                            }
                        }
                    ]
                }
            }
        }
    return data

def ListMessage(number):
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": "✅ I have these options"
                },
                "footer": {
                    "text": "Select an option"
                },
                "action": {
                    "button": "See options",
                    "sections": [
                        {
                            "title": "Buy and sell products",
                            "rows": [
                                {
                                    "id": "main-buy",
                                    "title": "Buy",
                                    "description": "Buy the best product your home"
                                },
                                {
                                    "id": "main-sell",
                                    "title": "Sell",
                                    "description": "Sell your products"
                                }
                            ]
                        },
                        {
                            "title": "📍center of attention",
                            "rows": [
                                {
                                    "id": "main-agency",
                                    "title": "Agency",
                                    "description": "Your can visit our agency"
                                },
                                {
                                    "id": "main-contact",
                                    "title": "Contact center",
                                    "description": "One of our agents will assist you"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    return data
