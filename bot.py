
import os
import requests
from datetime import datetime, timedelta

def buscar_vuelos():
    origen = "MVD" # Montevideo
    destino = "MIA" # Miami
    pasajeros = 3
    
    # Buscamos una fecha de muestra a 3 meses desde hoy para ver tarifas estables
    fecha_viaje = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
    
    try:
        # Consulta rápida a motor de tarifas referenciales en USD
        url = f"https://api.skypicker.com/flights?fly_from={origen}&to={destino}&date_from={fecha_viaje}&date_to={fecha_viaje}&passengers={pasajeros}&curr=USD&limit=1"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            datos = response.json()
            if "data" in datos and datos["data"]:
                vuelo = datos["data"][0]
                precio_total = vuelo["price"]
                aerolinea = vuelo.get("airlines", ["Regular"])[0]
                
                mensaje = (
                    f"✈️ *¡ALERTA DE VUELOS MVD -> MIA!* ✈️\n\n"
                    f"👥 *Pasajeros:* {pasajeros} personas\n"
                    f"📅 *Fecha de muestra:* {fecha_viaje}\n"
                    f"💰 *Mejor precio TOTAL:* USD {precio_total}\n"
                    f"🏢 *Aerolínea:* {aerolinea}\n\n"
                    f" _Este es el precio más bajo detectado hoy automáticamente._"
                )
                return mensaje
    except Exception as e:
        return f"⚠️ Error en el radar de vuelos: {str(e)}"
    
    return "✈️ *Radar de Vuelos MVD ➔ MIA*\n\nNo se pudieron obtener tarifas en este momento. Reintentando en el próximo turno automático."

def enviar_telegram(mensaje):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    reporte = buscar_vuelos()
    enviar_telegram(reporte)

