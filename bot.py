
import os
import requests
from datetime import datetime

def buscar_vuelos():
    origen = "MVD"  # Montevideo
    destino = "MIA" # Miami
    pasajeros = 3
    
    # Configuramos el rango flexible para febrero 2026
    fecha_desde = "01/02/2026"
    fecha_hasta = "28/02/2026"
    
    # Tus 20 días planeados con el margen de 3 días hacia atrás y adelante (17 a 23 días de estadía)
    estadia_min = 17
    estadia_max = 23
    
    try:
        # Usamos la API de Kiwi con parámetros de rango de fechas y estadía flexible
        url = (
            f"https://api.skypicker.com/flights?"
            f"fly_from={origen}&to={destino}&"
            f"date_from={fecha_desde}&date_to={fecha_hasta}&"
            f"days_in_安定_from={estadia_min}&days_in_安定_to={estadia_max}&"
            f"passengers={pasajeros}&curr=USD&limit=3&sort=price"
        )
        # Corrección técnica para la API de Kiwi (days_in_stay)
        url = url.replace("安定", "stay")
        
        response = requests.get(url, timeout=20)
        
        if response.status_code == 200:
            datos = response.json()
            if "data" in datos and datos["data"]:
                # Tomamos la opción más barata del rango encontrado
                mejor_vuelo = datos["data"][0]
                precio_total = mejor_vuelo["price"]
                
                # Extraemos las fechas exactas que encontró el buscador
                fecha_salida_unix = mejor_vuelo["route"][0]["dTime"]
                fecha_salida = datetime.fromtimestamp(fecha_salida_unix).strftime('%d/%m/%Y')
                
                # Buscamos el vuelo de regreso en la ruta para saber cuándo vuelve
                fecha_regreso_unix = mejor_vuelo["route"][-1]["dTime"]
                fecha_regreso = datetime.fromtimestamp(fecha_regreso_unix).strftime('%d/%m/%Y')
                
                aerolinea = mejor_vuelo.get("airlines", ["Regular"])[0]
                
                mensaje = (
                    f"✈️ *¡RADAR DE VUELOS FEBRERO 2026!* ✈️\n\n"
                    f"👥 *Pasajeros:* {pasajeros} personas\n"
                    f"🛫 *Salida ideal encontrada:* {fecha_salida}\n"
                    f"🛬 *Regreso:* {fecha_regreso}\n"
                    f"⏳ *Estadía:* {mejor_vuelo.get('nightsInDst')} noches\n"
                    f"💰 *Mejor precio TOTAL:* USD {precio_total}\n"
                    f"🏢 *Aerolínea:* {aerolinea}\n\n"
                    f" _Este precio cubre a las 3 personas en el rango flexible de febrero._"
                )
                return mensaje
    except Exception as e:
        return f"⚠️ Error en el radar de vuelos: {str(e)}"
    
    return "✈️ *Radar de Vuelos MVD ➔ MIA*\n\nNo se detectaron tarifas disponibles para febrero en este momento. Reintentando en el próximo turno automático."

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

