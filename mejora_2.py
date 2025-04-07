from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from datetime import datetime

# Iniciar el servicio de ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Lista de ubicaciones a buscar
ubicaciones = [
    {"nombre": "Benito Juárez", "lat": 19.371992, "lng": -99.157853},
    {"nombre": "Coyoacán", "lat": 19.350214, "lng": -99.162146},
    {"nombre": "Cuauhtémoc", "lat": 19.441646, "lng": -99.151884},
    {"nombre": "Miguel Hidalgo", "lat": 19.407269, "lng": -99.190754},
    {"nombre": "Tlalpan", "lat": 19.288275, "lng": -99.167125},
    {"nombre": "Polanco", "lat": 19.43353, "lng": -99.190915},
    {"nombre": "Roma", "lat": 19.386144, "lng": -99.174169},
    {"nombre": "Condesa", "lat": 19.4125, "lng": -99.1694},
    {"nombre": "Juárez", "lat": 19.42755, "lng": -99.16088},
]

# Lista para guardar los resultados
data = []

# Función para desplazamiento automático en barra lateral
def desplazamiento_infinito():
    try:
        panel_resultados = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
        prev_count = 0

        while True:
            driver.execute_script("arguments[0].scrollBy(0, 2500);", panel_resultados)
            time.sleep(3)
            cafeterias = driver.find_elements(By.CSS_SELECTOR, ".Nv2PK")

            if len(cafeterias) == prev_count:
                break

            prev_count = len(cafeterias)
    except Exception as e:
        print(f"Error durante el desplazamiento: {e}")

# Iterar sobre cada ubicación
for ubicacion in ubicaciones:
    print(f"\nBuscando cafeterías en {ubicacion['nombre']}...")
    url = f"https://www.google.com/maps/search/cafeterías/@{ubicacion['lat']},{ubicacion['lng']},14z"
    driver.get(url)
    time.sleep(10)  # Esperar carga inicial
    desplazamiento_infinito()

    cafeterias = driver.find_elements(By.CSS_SELECTOR, ".Nv2PK")
    print(f"{len(cafeterias)} cafeterías encontradas en {ubicacion['nombre']}.")

    for cafeteria in cafeterias:
        try:
            nombre = cafeteria.find_element(By.CSS_SELECTOR, ".qBF1Pd").text
            direccion = cafeteria.find_element(By.CSS_SELECTOR, ".W4Efsd").text

            # Extraer sitio web (si está disponible)
            try:
                sitio_web_element = cafeteria.find_element(By.CSS_SELECTOR, "a[href^='https://']")
                sitio_web = sitio_web_element.get_attribute("href")
            except:
                sitio_web = "No disponible"

            data.append({
                "Nombre": nombre,
                "Dirección": direccion,
                "Sitio web": sitio_web,
                "Zona": ubicacion["nombre"]
            })

        except Exception as e:
            print(f"Error extrayendo datos de una cafetería: {e}")

    time.sleep(5)  # Pausa entre zonas

# Guardar resultados si se encontraron datos
if data:
    df = pd.DataFrame(data)
    nombre_archivo = f"cafeterias_CDMX_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(nombre_archivo, index=False, engine='openpyxl')
    print(f"\n✅ Datos exportados exitosamente a '{nombre_archivo}'.")
else:
    print("\n⚠ No se encontraron datos para exportar.")

# Cerrar navegador
driver.quit()
