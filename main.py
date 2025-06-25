import requests
from bs4 import BeautifulSoup
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk.configuration import Configuration

URL = "https://www.cafonline.com/caf-africa-cup-of-nations/news/"
KEYWORDS = ["ticket", "tickets", "sale", "bamey"]  # ✅ Liste de mots-clés

API_KEY = os.environ.get("BREVO_API_KEY")
TO_EMAIL = os.environ.get("EMAIL")
FROM_EMAIL = os.environ.get("EMAIL")

def send_email(subject, content):
    configuration = Configuration()
    configuration.api_key['api-key'] = API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": TO_EMAIL}],
        sender={"email": FROM_EMAIL},
        subject=subject,
        text_content=content
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Email envoyé avec succès. ID:", api_response.message_id)
    except ApiException as e:
        print("Exception lors de l'envoi de l'email:", e)

res = requests.get(URL)
soup = BeautifulSoup(res.text, 'html.parser')
page_text = soup.text.lower()

# 🔍 Vérifie si un mot-clé est trouvé
found_keywords = [kw for kw in KEYWORDS if kw.lower() in page_text]

if found_keywords:
    found_str = ", ".join(found_keywords)
    send_email(
        "🎟️ Mots-clés détectés pour CAN 2025 !",
        f"Les mots-clés suivants ont été trouvés sur {URL} : {found_str}"
    )
    print("Mots-clés détectés :", found_str)
else:
    print("Aucun mot-clé détecté")
