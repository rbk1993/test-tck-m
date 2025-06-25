import os
from requests_html import HTMLSession
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk.configuration import Configuration

# URL à surveiller
URL = "https://www.cafonline.com/caf-africa-cup-of-nations/news/"

# Mots-clés à détecter
KEYWORDS = [
    "ticket", "tickets", "sale", "buy", "purchase",
    "available", "book", "ticketing", "admission", "access",
    "launch", "highlights"
]

# Clés et identifiants
BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
TO_EMAIL = os.environ.get("EMAIL")
FROM_EMAIL = os.environ.get("EMAIL")
SMS_TO_PHONE = os.environ.get("SMS_TO_PHONE")
SMS_SENDER = os.environ.get("SMS_SENDER")   # Exemple : "BREVO" ou numéro validé

# Envoi d'un SMS via Brevo
def send_sms(message):
    configuration = Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalSMSApi(sib_api_v3_sdk.ApiClient(configuration))
    sms_params = {
        "sender": SMS_SENDER,
        "recipient": SMS_TO_PHONE,
        "content": message,
        "type": "transactional"
    }

    try:
        api_response = api_instance.send_transac_sms(sms_params)
        print("SMS envoyé avec succès. ID:", api_response['messageId'])
    except ApiException as e:
        print("Erreur lors de l'envoi du SMS:", e.body)

# Envoi d'un email (non utilisé ici)
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

# Scraping JS avec Chromium headless
session = HTMLSession()
response = session.get(URL)
response.html.render(timeout=30, sleep=2)

text = response.html.text.lower()
found_keywords = [kw for kw in KEYWORDS if kw in text]

if found_keywords:
    message = f"🎟️ Mots-clés détectés ({', '.join(found_keywords)}) sur le site CAF: {URL}"
    print(message)
    send_sms(message)
else:
    print("Aucun mot-clé détecté")
