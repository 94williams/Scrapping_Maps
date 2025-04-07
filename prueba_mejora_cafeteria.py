from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Configuración de Selenium con Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Inicializar WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Lista de ubicaciones a buscar (en coordenadas latitud, longitud)
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

# Lista para almacenar datos
data = []

# Función para desplazarse hasta que no haya más resultados
def desplazamiento_infinito():
    try:
        # Localizar el contenedor donde están los resultados
        panel_resultados = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
        prev_count = 0  # Contador de cafeterías previas

        while True:
            # Desplazar la barra lateral hasta el final
            driver.execute_script("arguments[0].scrollBy(0, 1000);", panel_resultados)
            time.sleep(15)  # Espera para permitir la carga de nuevos resultados

            # Contar los elementos actuales en la lista
            cafeterias = driver.find_elements(By.CSS_SELECTOR, ".Nv2PK")

            # Si después del desplazamiento el número de cafeterías sigue igual, significa que no hay más resultados
            if len(cafeterias) == prev_count:
                print("No hay más resultados, deteniendo scroll.")
                break

            prev_count = len(cafeterias)  # Actualizar el conteo de cafeterías

    except Exception as e:
        print(f"Error durante el desplazamiento: {e}")



# Iterar sobre las ubicaciones
for ubicacion in ubicaciones:
    print(f"Buscando cafeterías en {ubicacion['nombre']}...")
    url = f"https://www.google.com/maps/search/cafeterías/@{ubicacion['lat']},{ubicacion['lng']},14z"
    driver.get(url)
    
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".Nv2PK"))
        )
    except:
        print(f"No se encontraron cafeterías en {ubicacion['nombre']}.")
        continue
    
    desplazamiento_infinito()
    
    cafeterias = driver.find_elements(By.CSS_SELECTOR, ".Nv2PK")
    print(f"Se encontraron {len(cafeterias)} cafeterías en {ubicacion['nombre']}.")
    
for cafeteria in cafeterias:
    try:
        nombre = cafeteria.find_element(By.CSS_SELECTOR, ".qBF1Pd").text
        direccion = cafeteria.find_element(By.CSS_SELECTOR, ".W4Efsd").text
        
        # Intentar extraer el enlace del sitio web
        try:
            sitio_web_element = cafeteria.find_element(By.CSS_SELECTOR, "a[href^='https://']")
            sitio_web = sitio_web_element.get_attribute("href")
        except:
            sitio_web = "No disponible"

        # Guardar datos en la lista
        data.append({
            "Nombre": nombre,
            "Dirección": direccion,
            "Sitio web": sitio_web,
            "Zona": ubicacion["nombre"]
        })

    except Exception as e:
        print(f"Error extrayendo datos: {e}")

# Guardar datos en un archivo Excel
df = pd.DataFrame(data)
df.to_excel("cafeterias_CDMX.xlsx", index=False, engine='openpyxl')
print("Datos exportados a cafeterias_CDMX.xlsx")

# Cerrar navegador
driver.quit()
