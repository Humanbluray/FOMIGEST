import requests
import time

# Remplace l'URL ci-dessous par l'URL de ton application Railway
APP_URL = "https://fomigest-production.up.railway.app/"

while True:
    try:
        response = requests.get(APP_URL)
        print(f"Ping réussi : {response.status_code}")
    except Exception as e:
        print(f"Erreur de ping : {e}")
    time.sleep(300)  # Ping toutes les 5 minutes
