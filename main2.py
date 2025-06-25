from requests_html import HTMLSession
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk.configuration import Configuration

# Configuration générale
URL = "https://www.cafonline.com/caf-africa-cup-of-nations/news/"
KEYWORDS = ["ticket", "tickets", "sale", "highlights"]

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

# Scraping avec requests-html
def fetch_rendered_html(url):
    session = HTMLSession()
    response = session.get(url)
    response.html.render(timeout=30)  # Rend la page avec JS (via pyppeteer)
    return response.html.html

# Lancer le scraping
print("Chargement de la page...")
rendered_html = fetch_rendered_html(URL)
lowered_html = rendered_html.lower()

# Recherche des mots-clés
matched_keywords = [kw for kw in KEYWORDS if kw.lower() in lowered_html]
if matched_keywords:
    print("Mots-clés détectés :", matched_keywords)
    send_email(
        "🎟️ Mots-clés CAN détectés !",
        f"Les mots-clés suivants ont été trouvés sur la page : {', '.join(matched_keywords)}\n\nURL : {URL}"
    )
else:
    print("Aucun mot-clé détecté.")
