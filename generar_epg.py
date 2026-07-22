import xml.etree.ElementTree as ET
import urllib.request

# Usamos la fuente oficial y estable de iptv-org para España (XML sin comprimir)
URL_EPG = "https://github.io"

def filtrar_canales():
    print("Descargando EPG base desde iptv-org...")
    
    # Añadimos un User-Agent para que el servidor no bloquee la descarga automatizada
    req = urllib.request.Request(URL_EPG, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        xml_data = response.read()
            
    print("Leyendo tu archivo de canales favoritos...")
    with open("canales.txt", "r", encoding="utf-8") as f:
        mis_canales = [linea.strip() for linea in f if linea.strip()]

    print(f"Canales que vas a buscar: {mis_canales}")

    root = ET.fromstring(xml_data)
    nuevo_xml = ET.Element("tv", root.attrib)
    
    # 1. Filtrar y añadir los canales que coincidan
    id_canales_encontrados = set()
    for canal in root.findall("channel"):
        display_name = canal.find("display-name")
        canal_id = canal.get("id")
        
        # Comprobamos si el nombre del canal en el XML coincide con tu lista favorita
        if display_name is not None and display_name.text in mis_canales:
            nuevo_xml.append(canal)
            id_canales_encontrados.add(canal_id)
            
    # 2. Filtrar y añadir la programación solo de esos canales encontrados
    for programa in root.findall("programme"):
        prog_canal_id = programa.get("channel")
        if prog_canal_id in id_canales_encontrados:
            nuevo_xml.append(programa)
            
    # Guardar tu guía limpia
    nuevo_arbol = ET.ElementTree(nuevo_xml)
    nuevo_arbol.write("guiatv.xml", encoding="utf-8", xml_declaration=True)
    print("¡Archivo guiatv.xml generado con éxito!")

if __name__ == "__main__":
    filtrar_canales()
