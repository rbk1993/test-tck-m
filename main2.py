from requests_html import HTMLSession
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk.configuration import Configuration

URL = "https://www.cafonline.com/caf-africa-cup-of-nations/news/"
KEYWORDS = ["ticket", "tickets", "sale", "highlights", "bamey", "ckets", "sal"]

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
TO_EMAIL = os.environ.get("EMAIL")
FROM_EMAIL = os.environ.get("EMAIL")

def send_email(subject, content):
    configuration = Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY
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

# 1. Crée une session HTML
session = HTMLSession()
response = session.get(URL)

# 2. Rend la page (JavaScript)
response.html.render(timeout=30, sleep=2)  # Optionnel : augmenter si page lente

# 3. Vérifie les mots-clés dans le contenu rendu
page_text = response.html.text.lower()
found_keywords = [kw for kw in KEYWORDS if kw.lower() in page_text]

if found_keywords:
    send_email("🎟️ Billets CAN 2025 détectés !", f"Mots-clés détectés : {', '.join(found_keywords)} sur {URL}")
    print("✅ Mots-clés détectés :", found_keywords)
else:
    print("Aucun mot-clé détecté")
