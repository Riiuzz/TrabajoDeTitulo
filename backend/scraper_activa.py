"""
Script para descargar y almacenar contenido de Activa Research en MongoDB.
Este script extrae información de las páginas principales de Activa Research
y la guarda en una colección de MongoDB para que el bot pueda consultarla.
"""

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME", "trabajo_titulo")

# URLs a descargar
URLS_TO_SCRAPE = {
    "pulso_ciudadano": "https://chile.activasite.com/pulso-ciudadano/",
    "estudios": "https://chile.activasite.com/estudios-de-opinion/",
    "quienes_somos": "https://chile.activasite.com/quienes-somos/"
}

# Headers para simular un navegador real
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def conectar_mongodb():
    """Conecta a MongoDB y retorna la colección."""
    try:
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DBNAME]
        return db["activa_content"], client
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {repr(e)}")
        return None, None


def descargar_contenido(url: str) -> str:
    """Descarga el HTML de una URL."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Error descargando {url}: {repr(e)}")
        return ""


def extraer_contenido_pulso(html: str) -> list:
    """Extrae información de Pulso Ciudadano."""
    soup = BeautifulSoup(html, "html.parser")
    contenido = []
    
    # Información general
    titulo = soup.find("h1")
    descripcion = soup.find("p")
    
    general = {
        "type": "pulso_ciudadano",
        "titulo": titulo.get_text(strip=True) if titulo else "Pulso Ciudadano",
        "descripcion": descripcion.get_text(strip=True) if descripcion else "",
    }
    contenido.append(general)
    
    # Estudios/reportes individuales
    articulos = soup.find_all("div", class_=["item-study", "study-card", "post"])
    
    for articulo in articulos[:10]:  # Limitar a 10 más recientes
        try:
            titulo_articulo = articulo.find("h3") or articulo.find("h4")
            link = articulo.find("a")
            fecha = articulo.find("span", class_=["date", "fecha"])
            
            if titulo_articulo:
                item = {
                    "type": "pulso_estudio",
                    "titulo": titulo_articulo.get_text(strip=True),
                    "enlace": link["href"] if link else "",
                    "fecha": fecha.get_text(strip=True) if fecha else "",
                }
                contenido.append(item)
        except Exception as e:
            print(f"⚠️  Error extrayendo estudio: {repr(e)}")
            continue
    
    return contenido


def extraer_contenido_estudios(html: str) -> list:
    """Extrae información de Estudios de Opinión."""
    soup = BeautifulSoup(html, "html.parser")
    contenido = []
    
    # Información general
    titulo = soup.find("h1")
    descripcion = soup.find("p")
    
    general = {
        "type": "estudios_opinion",
        "titulo": titulo.get_text(strip=True) if titulo else "Estudios de Opinión",
        "descripcion": descripcion.get_text(strip=True) if descripcion else "",
    }
    contenido.append(general)
    
    # Estudios individuales
    articulos = soup.find_all("div", class_=["item-study", "study-card", "post"])
    
    for articulo in articulos[:10]:
        try:
            titulo_articulo = articulo.find("h3") or articulo.find("h4")
            link = articulo.find("a")
            fecha = articulo.find("span", class_=["date", "fecha"])
            
            if titulo_articulo:
                item = {
                    "type": "estudio_individual",
                    "titulo": titulo_articulo.get_text(strip=True),
                    "enlace": link["href"] if link else "",
                    "fecha": fecha.get_text(strip=True) if fecha else "",
                }
                contenido.append(item)
        except Exception as e:
            print(f"⚠️  Error extrayendo estudio: {repr(e)}")
            continue
    
    return contenido


def extraer_contenido_quienes_somos(html: str) -> list:
    """Extrae información de Quiénes Somos."""
    soup = BeautifulSoup(html, "html.parser")
    contenido = []
    
    # Información general - Especialidades
    especialidades = soup.find_all("h3")
    
    general = {
        "type": "quienes_somos",
        "titulo": "Activa Research - Quiénes Somos",
        "especialidades": [e.get_text(strip=True) for e in especialidades[:8]],
    }
    contenido.append(general)
    
    # Áreas de experiencia
    areas = ["Business Intelligence y Data Analytics", 
             "Online and Digital Research",
             "Crowdsourcing",
             "Dashboard y Web Report",
             "Branding y Comunicación",
             "Experiencia",
             "Innovación",
             "Opinión pública"]
    
    for area in areas:
        if area.lower() in html.lower():
            item = {
                "type": "area_experiencia",
                "nombre": area,
                "categoria": "quienes_somos"
            }
            contenido.append(item)
    
    # Descripción de servicios
    parrafos = soup.find_all("p")
    for parrafo in parrafos[:5]:
        texto = parrafo.get_text(strip=True)
        if len(texto) > 100:  # Solo párrafos sustanciales
            contenido.append({
                "type": "descripcion_servicio",
                "texto": texto,
                "categoria": "quienes_somos"
            })
    
    return contenido


def guardar_contenido(coleccion, section_key: str, contenido: list):
    """Guarda el contenido en MongoDB."""
    try:
        # Eliminar contenido anterior de esta sección
        coleccion.delete_many({"seccion": section_key})
        
        # Insertar nuevo contenido
        for item in contenido:
            doc = {
                "seccion": section_key,
                "contenido": item,
                "fecha_actualizacion": datetime.now()
            }
            coleccion.insert_one(doc)
        
        print(f"✅ {len(contenido)} documentos guardados para {section_key}")
        
    except Exception as e:
        print(f"❌ Error guardando contenido: {repr(e)}")


def main():
    """Función principal que ejecuta el scraping."""
    print("🔄 Iniciando descarga de contenido de Activa Research...")
    
    # Conectar a MongoDB
    coleccion, cliente = conectar_mongodb()
    if coleccion is None:
        print("❌ No se pudo conectar a MongoDB. Abortando.")
        return
    
    # Descargar y procesar cada sección
    for section_key, url in URLS_TO_SCRAPE.items():
        print(f"\n📥 Procesando: {section_key}")
        print(f"   URL: {url}")
        
        # Descargar HTML
        html = descargar_contenido(url)
        if not html:
            print(f"❌ No se pudo descargar {section_key}")
            continue
        
        # Extraer contenido según el tipo
        if section_key == "pulso_ciudadano":
            contenido = extraer_contenido_pulso(html)
        elif section_key == "estudios":
            contenido = extraer_contenido_estudios(html)
        else:  # quienes_somos
            contenido = extraer_contenido_quienes_somos(html)
        
        # Guardar en MongoDB
        guardar_contenido(coleccion, section_key, contenido)
    
    # Cerrar conexión
    cliente.close()
    print("\n✅ Descarga completada!")


if __name__ == "__main__":
    main()
