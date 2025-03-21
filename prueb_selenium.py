from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # Instalar webdriver-manager

# Crear el servicio usando el gestor de drivers de Chrome
service = Service(ChromeDriverManager().install())

# Iniciar el navegador usando el servicio
driver = webdriver.Chrome(service=service)

# Abre una página web
driver.get("https://www.google.com")

# Realiza las acciones que necesitas

