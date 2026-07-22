import urllib.request
import re
from datetime import datetime

def generar_epg_directo():
    print("Iniciando generador de canales favoritos...")
    
    # 1. Definimos las fechas en formato XMLTV (AñoMesDía)
    hoy = datetime.now().strftime("%Y%m%d")
    
    # 2. Generamos el texto XML directamente para evitar errores de lectura
    xml_lineas = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<tv generator-info-name="MiAutogenerador">',
        '  <channel id="La1"><display-name>La 1</display-name></channel>',
        '  <channel id="Antena3"><display-name>Antena 3</display-name></channel>',
        '  <channel id="Cuatro"><display-name>Cuatro</display-name></channel>',
        '  <channel id="Telecinco"><display-name>Telecinco</display-name></channel>',
        '  <channel id="LaSexta"><display-name>La Sexta</display-name></channel>'
    ]
    
    # 3. Agregamos bloques de programación genérica segura de 24 horas para que tu IPTV siempre tenga datos
    canales_ids = ["La1", "Antena3", "Cuatro", "Telecinco", "LaSexta"]
    canales_nombres = ["La 1", "Antena 3", "Cuatro", "Telecinco", "La Sexta"]
    
    for c_id, c_name in zip(canales_ids, canales_nombres):
        xml_lineas.append(f'  <programme start="{hoy}060000 +0000" stop="{hoy}150000 +0000" channel="{c_id}"><title lang="es">Programación de Mañana - {c_name}</title><desc lang="es">Magacines, informativos y entretenimiento en directo.</desc></programme>')
        xml_lineas.append(f'  <programme start="{hoy}150000 +0000" stop="{hoy}210000 +0000" channel="{c_id}"><title lang="es">Cine y Entretenimiento de Tarde - {c_name}</title><desc lang="es">Películas, series y actualidad de la tarde.</desc></programme>')
        xml_lineas.append(f'  <programme start="{hoy}210000 +0000" stop="{hoy}235959 +0000" channel="{c_id}"><title lang="es">Contenido Estrella de Noche - {c_name}</title><desc lang="es">Grandes estrenos, debates o el mejor prime time.</desc></programme>')

    xml_lineas.append('</tv>')
    
    # 4. Escribimos el archivo final de corrido
    contenido_total = "\n".join(xml_lineas)
    with open("guiatv.xml", "w", encoding="utf-8") as f:
        f.write(contenido_total)
        
    print("¡Archivo guiatv.xml escrito de forma directa con éxito!")

if __name__ == "__main__":
    generar_epg_directo()
