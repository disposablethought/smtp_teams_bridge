import asyncio
import logging
import os
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP as SMTPServer
from email import message_from_bytes
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebhookHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        try:
            email_message = message_from_bytes(envelope.content)
            
            # Extract subject and body
            subject = email_message.get('subject', 'No Subject')
            
            # Get body (prefer plain text, fall back to HTML)
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
                    elif part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = email_message.get_payload(decode=True).decode()

            # Format message for Teams webhook
            teams_message = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "summary": subject,
                "themeColor": "0076D7",
                "sections": [{
                    "activityTitle": subject,
                    "text": body
                }]
            }

            # Send to webhook
            webhook_url = os.getenv('WEBHOOK_URL')
            if not webhook_url:
                raise ValueError("WEBHOOK_URL environment variable not set")

            response = requests.post(webhook_url, json=teams_message)
            response.raise_for_status()
            
            logger.info(f"Successfully sent message. Subject: {subject}")
            return '250 Message accepted for delivery'
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return '500 Error processing message'

async def start_smtp_server():
    handler = WebhookHandler()
    controller = Controller(
        handler,
        hostname='0.0.0.0',
        port=int(os.getenv('SMTP_PORT', '25')),
        server_kwargs={'enable_SMTPUTF8': True}
    )
    
    controller.start()
    logger.info(f"SMTP server started on port {controller.port}")
    
    # Keep the server running
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    load_dotenv()
    asyncio.run(start_smtp_server())
