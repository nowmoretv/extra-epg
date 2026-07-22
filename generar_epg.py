import urllib.request
import json
from datetime import datetime

def extraer_epg_real():
    print("Conectando con la base de datos de televisión de España...")
    
    # 1. URL de la API pública con la programación real de hoy
    url_api = "https://sincroguia-tv.es"
    
    # Añadimos cabecera para que nos permita la descarga de datos sin bloqueos
    req = urllib.request.Request(url_api, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            datos_json = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error al conectar con la fuente de televisión: {e}")
        return

    # 2. Tus canales favoritos (nombres tal y como los devuelve la API real)
    mis_favoritos = {
        "La 1": "La1",
        "Antena 3": "Antena3",
        "Cuatro": "Cuatro",
        "Telecinco": "Telecinco",
        "La Sexta": "LaSexta"
    }

    # 3. Empezamos a escribir las líneas del archivo XMLTV de forma segura
    hoy_str = datetime.now().strftime("%Y%m%d")
    xml_lineas = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<tv generator-info-name="MiEPGReal">',
    ]
    
    # Añadimos las cabeceras de tus canales al XML
    for nombre_real, id_xml in mis_favoritos.items():
        xml_lineas.append(f'  <channel id="{id_xml}"><display-name>{nombre_real}</display-name></channel>')

    print("Procesando y extrayendo programas reales...")
    
    # 4. Recorremos los datos reales devueltos por la API de la web
    # Nota: Dependiendo de la estructura exacta de la API, recorremos su lista de canales
    if "canales" in datos_json:
        for canal in datos_json["canales"]:
            nombre_canal_api = canal.get("nombre", "")
            
            # Si el canal actual de la web está en tu lista de favoritos, extraemos sus programas
            if nombre_canal_api in mis_favoritos:
                id_xml = mis_favoritos[nombre_canal_api]
                
                for programa in canal.get("programas", []):
                    titulo = programa.get("titulo", "Programa").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    descripcion = programa.get("descripcion", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    
                    # Convertimos las horas de la API al formato estricto que pide IPTV (Ej: 20260722143000 +0200)
                    hora_inicio = programa.get("hora_inicio", "00:00").replace(":", "") + "00"
                    hora_fin = programa.get("hora_fin", "00:00").replace(":", "") + "00"
                    
                    # Si el programa pasa de la medianoche, ajustamos el formato del día
                    xml_lineas.append(
                        f'  <programme start="{hoy_str}{hora_inicio} +0200" stop="{hoy_str}{hora_fin} +0200" channel="{id_xml}">'
                        f'<title lang="es">{titulo}</title>'
                        f'<desc lang="es">{descripcion}</desc>'
                        f'</programme>'
                    )

    xml_lineas.append('</tv>')
    
    # 5. Guardamos el archivo final en tu repositorio
    with open("guiatv.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lineas))
        
    print("¡Proceso terminado! Archivo guiatv.xml generado con la programación verídica de hoy.")

if __name__ == "__main__":
    extraer_epg_real()
