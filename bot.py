
import os
import requests
import yfinance as yf

# 1. CONFIGURACIÓN DEL BOT DE TELEGRAM
# GitHub guarda de forma segura tu Token y tu ID de Chat para que nadie los vea.
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 2. TU LISTA DE COMPRAS (Acá elegís qué mirar y a qué precio está "barata")
# El formato es: "TICKER": Precio_Máximo_A_Pagar
# Podés cambiar los números y las empresas cuando quieras.
ACCIONES_A_MONITOREAR = {
    "RBLX": 35.0, # Roblox: Avisame si baja de 35 dólares
    "NFLX": 600.0, # Netflix: Avisame si baja de 600 dólares
    "CAN": 1.5 # Canaan (Crypto/Minería): Avisame si baja de 1.5 dólares
}

def enviar_alerta_telegram(mensaje):
    """Esta función se encarga de mandar el mensaje a tu celular"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error al enviar a Telegram: {e}")

def revisar_mercado():
    """Esta función mira los precios reales en Yahoo Finance y compara"""
    print("Iniciando revisión de precios...")
    mensajes_alerta = []

    for empresa, precio_barato in ACCIONES_A_MONITOREAR.items():
        try:
            # Buscamos la información de la acción en Yahoo Finance
            ticker = yf.Ticker(empresa)
            # Tomamos el último precio de cierre del mercado
            precio_actual = ticker.history(period="1d")["Close"].iloc[-1]
            
            print(f"{empresa}: Precio actual es {precio_actual:.2f} USD (Tu límite es {precio_barato} USD)")

            # SI EL PRECIO ACTUAL ES MENOR O IGUAL AL QUE VOS QUERÉS, SE ACTIVA LA ALERTA
            if precio_actual <= precio_barato:
                mensajes_alerta.append(f"🚨 ¡OFERTA! {empresa} está a {precio_actual:.2f} USD (Precio objetivo: {precio_barato} USD)")
        
        except Exception as e:
            print(f"No se pudo revisar {empresa}: {e}")

    # Si encontramos acciones baratas, mandamos el mensaje reunido
    if mensajes_alerta:
        mensaje_final = "📈 Alertas de Acciones Baratas:\n\n" + "\n".join(mensajes_alerta)
        enviar_alerta_telegram(mensaje_final)
        print("¡Alertas enviadas a Telegram!")
    else:
        print("Todo normal, ninguna acción alcanzó el precio de oferta.")

# Esto le dice a Python que ejecute la revisión cuando GitHub Actions active el script
if __name__ == "__main__":
    revisar_mercado()

