

import requests

TOKEN = "8980218948:AAF3SmcMxlz4aYXjAoJXFnQ_FfM98_e6Zic"
CHAT_ID = "6219209932"

mensaje = "🚀 Hola Gabriel, tu sistema de alertas está funcionando."

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": mensaje
})

print("Mensaje enviado")

