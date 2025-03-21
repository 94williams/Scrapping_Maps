from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Usamos webdriver_manager para obtener y manejar ChromeDriver automáticamente
driver_path = ChromeDriverManager().install()

# Crear un servicio con la ruta del ChromeDriver
service = Service(driver_path)

# Inicia el navegador con Selenium usando el servicio
driver = webdriver.Chrome(service=service)

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
    {"nombre": "Santa María la Ribera", "lat": 19.44935, "lng": -99.157275},
    {"nombre": "Del Valle", "lat": 19.38611, "lng": -99.16204},
    {"nombre": "San Miguel Chapultepec", "lat": 19.411473, "lng": -99.188521},
    {"nombre": "Reforma", "lat": 19.430546, "lng": -99.161421},
    {"nombre": "Santa Fe", "lat": 19.399056, "lng": -99.1982303},
    {"nombre": "Álvaro Obregón", "lat": 19.390806, "lng": -99.195413},
    {"nombre": "Azcapotzalco", "lat": 19.484102, "lng": -99.18436},
    {"nombre": "Cuajimalpa de Morelos", "lat": 19.35735, "lng": -99.299792},
    {"nombre": "Gustavo A. Madero", "lat": 19.482945, "lng": -99.113471},
    {"nombre": "Iztacalco", "lat": 19.395901, "lng": -99.097612},
    {"nombre": "Iztapalapa", "lat": 19.359004, "lng": -99.092622},
    {"nombre": "La Magdalena Contreras", "lat": 19.304898, "lng": -99.241515},
    {"nombre": "Milpa Alta", "lat": 19.191249, "lng": -99.023371},
    {"nombre": "Tláhuac", "lat": 19.270566, "lng": -99.004846},
    {"nombre": "Venustiano Carranza", "lat": 19.419261, "lng": -99.113701},
    {"nombre": "Xochimilco", "lat": 19.263462, "lng": -99.104913},
    {"nombre": "Tlalnepantla", "lat": 19.5825, "lng": -99.2217},
]

# Creamos una lista para almacenar la información de las cafeterías
data = []

# Iterar sobre las ubicaciones
for ubicacion in ubicaciones:
    print(f"Buscando cafeterías en {ubicacion['nombre']}...")

    # Construir la URL para cada ubicación con coordenadas lat, lng
    url = f"https://www.google.com/maps/search/cafeterías/@{ubicacion['lat']},{ubicacion['lng']},14z"
    driver.get(url)

    # Espera para que la página cargue completamente
    time.sleep(15)

    # Desplazamiento hacia abajo para cargar más resultados
    for _ in range(30):  # Ajusta el número de veces que el navegador se desplazará hacia abajo
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(5)

    # Extrae los elementos que contienen la información de las cafeterías
    cafeterias = driver.find_elements(By.CSS_SELECTOR, ".Nv2PK")

    # Verifica si hay cafeterías encontradas
    if cafeterias:
        print(f"Se encontraron {len(cafeterias)} cafeterías en {ubicacion['nombre']}.\n")

        # Iterar sobre los resultados encontrados
        for cafeteria in cafeterias:
            try:
                nombre = cafeteria.find_element(By.CSS_SELECTOR, ".qBF1Pd").text
                direccion = cafeteria.find_element(By.CSS_SELECTOR, ".W4Efsd").text
                tipo_comida = "No disponible"  # No se puede obtener directamente en Google Maps

                # Intentamos obtener información adicional (correo y redes sociales)
                try:
                    # Buscar redes sociales (si están disponibles)
                    redes_sociales = cafeteria.find_elements(By.CSS_SELECTOR, "a[href*='facebook.com'], a[href*='instagram.com'], a[href*='twitter.com']")
                    redes = [red.get_attribute('href') for red in redes_sociales]
                    correo = "No disponible"  # No se puede obtener fácilmente desde Google Maps

                except Exception as e:
                    redes = []
                    correo = "No disponible"
                    print(f"Error al extraer redes sociales o correo: {e}")

                # Agregar los datos a la lista
                data.append({
                    "Nombre": nombre,
                    "Dirección": direccion,
                    "Tipo de comida": tipo_comida,
                    "Correo electrónico": correo,
                    "Redes sociales": ", ".join(redes),
                    "Zona": ubicacion["nombre"]
                })

            except Exception as e:
                print(f"Error al extraer datos de un cafeteria: {e}")
    else:
        print(f"No se encontraron cafeterías en la zona de {ubicacion['nombre']}.")

# Crear un DataFrame con pandas
df = pd.DataFrame(data)

# Exportar los datos a un archivo Excel
df.to_excel("cafeterias_en_CDMX_zonas.xlsx", index=False, engine='openpyxl')
print(f"Los datos han sido exportados a 'cafeterias_en_CDMX_zonas.xlsx'.")

# Cerrar el navegador al finalizar
driver.quit()