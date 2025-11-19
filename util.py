def GetTextUser(message):
    text = ""
    typeMessage = message["type"]  

    if typeMessage == "text":
        text = (message["text"])["body"]   
    elif typeMessage == "interactive":
        interactiveObject = message["interactive"]
        interactiveType = interactiveObject["type"]

        if interactiveType == "button_reply":
            text = (interactiveObject["button_reply"])["title"]
        elif interactiveType == "list_reply":
            text = (interactiveObject["list_reply"])["title"]
        else:
            print("Sin mensaje")
            
    else:
        print("Sin mensaje")
    
    return text

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