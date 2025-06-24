import requests
from bs4 import BeautifulSoup
import os
from sendinblue_api import SendinBlueApi
from sendinblue_api.rest import ApiException

URL = "https://www.cafonline.com/caf-africa-cup-of-nations/news/"
KEYWORD = "tickets"

API_KEY = os.environ.get("BREVO_API_KEY")
TO_EMAIL = os.environ.get("EMAIL")
FROM_EMAIL = os.environ.get("EMAIL")

def send_email(subject, content):
    configuration = SendinBlueApi.Configuration()
    configuration.api_key['api-key'] = API_KEY
    api_instance = SendinBlueApi.TransactionalEmailsApi(SendinBlueApi.ApiClient(configuration))
    
    send_smtp_email = SendinBlueApi.SendSmtpEmail(
        to=[{"email": TO_EMAIL}],
        sender={"email": FROM_EMAIL},
        subject=subject,
        text_content=content
    )
    
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Email envoyé avec succès. ID:", api_response['messageId'])
    except ApiException as e:
        print("Exception lors de l'envoi de l'email:", e)

res = requests.get(URL)
soup = BeautifulSoup(res.text, 'html.parser')

if KEYWORD.lower() in soup.text.lower():
    send_email("🎟️ Billets CAN 2025 détectés !", f"Le mot-clé '{KEYWORD}' a été trouvé sur {URL}")
else:
    print("Pas encore disponible.")
