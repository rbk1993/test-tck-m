import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

URL = "https://webook.com/fr/explore?tag=football"
KEYWORD = "CAN"

EMAIL = os.environ.get("EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)

try:
    res = requests.get(URL, timeout=10)
    soup = BeautifulSoup(res.text, 'html.parser')

    if KEYWORD.lower() in soup.text.lower():
        send_email("🎟️ CAN 2025 - Billets détectés !", f"Billets potentiels trouvés ici : {URL}")
    else:
        print("Rien détecté pour le moment.")
except Exception as e:
    print(f"Erreur pendant l'exécution : {e}")
