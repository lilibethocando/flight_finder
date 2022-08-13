# This class is responsible for sending notifications with the deal flight details.

from twilio.rest import Client
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_VIRTUAL_NUMBER = os.getenv('TWILIO_VIRTUAL_NUMBER')
TWILIO_VERIFIED_NUMBER = os.getenv('TWILIO_VERIFIED_NUMBER')

MY_EMAIL = os.getenv('MY_EMAIL')
PASSWORD = os.getenv('PASSWORD')

class NotificationManager:
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)


    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP("smtp.office365.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New flight deal✈️\n\n{message}\n{google_flight_link}".encode('utf-8')
                )

