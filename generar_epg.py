import xml.etree.ElementTree as ET
import urllib.request
import gzip

# Fuente pública y estable de guías de TV de España
URL_EPG = "https://github.com"

def filtrar_canales():
    print("Descargando EPG base...")
    # Descargar el archivo comprimido (.gz) para ir rápido
    request = urllib.request.Request(URL_EPG, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request) as response:
        with gzip.GzipFile(fileobj=response) as unzipped:
            xml_data = unzipped.read()
            
    print("Filtrando tus favoritos...")
    with open("canales.txt", "r", encoding="utf-8") as f:
        mis_canales = [linea.strip() for linea in f if linea.strip()]

    root = ET.fromstring(xml_data)
    nuevo_xml = ET.Element("tv", root.attrib)
    
    # Añadir los canales que coincidan
    for canal in root.findall("channel"):
        display_name = canal.find("display-name")
        if display_name is not None and display_name.text in mis_canales:
            nuevo_xml.append(canal)
            
    # Añadir la programación de esos canales
    for programa in root.findall("programme"):
        # Buscamos si el ID del canal copiado coincide con los filtrados
        if any(prog_canal in mis_canales for prog_canal in mis_canales):
            nuevo_xml.append(programa)
            
    # Guardar archivo limpio
    nuevo_arbol = ET.ElementTree(nuevo_xml)
    nuevo_arbol.write("guiatv.xml", encoding="utf-8", xml_declaration=True)
    print("¡Guía generada con éxito!")

if __name__ == "__main__":
    filtrar_canales()
