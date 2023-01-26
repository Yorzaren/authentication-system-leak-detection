"""
This script is to send emails to a specified address when certain events happens

It uses a file called .env to hold secrets we don't want leaked out of production.

"""

import base64
import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

load_dotenv()  # Load the secrets from the .env file
sender_email = os.environ.get("sender_email")
sender_password = os.environ.get("sender_password")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")  # Name of the email we want to send the alerts to.


# More or less: https://mailtrap.io/blog/python-send-email-gmail/
# Requires us to re-login a lot but might work in a pinch
# Will open a window asking you to login and to be able to send on your behalf
# Only works on my whitelisted dev_account
def req_google_auth_send_email(recipient_email, email_subject, email_body):
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(email_body)
    message["to"] = recipient_email
    message["subject"] = email_subject

    create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(f"An error occurred: {error}")
        message = None


# Requires you to use commandline to open the port
# python -m smtpd -c DebuggingServer -n localhost:1025
def localhost_send_email(sender_email, recipient_email, email_subject, email_body):
    sender = sender_email
    receivers = recipient_email

    port = 1025
    msg = MIMEText(email_body)

    msg["Subject"] = email_subject
    msg["From"] = sender_email
    msg["To"] = recipient_email
    try:
        with smtplib.SMTP("localhost", port) as server:
            server.sendmail(sender, receivers, msg.as_string())
            print("Successfully sent email")
    except:
        print("Error: Cant send email\nIf using localhost run:\npython -m smtpd -c DebuggingServer -n localhost:1025")


# Google won't let us use this anymore with the deprecation of insecure app access.
def defunt_send_email(sender_email, sender_password, recipient_email, email_subject, email_body):
    subject = "Hello from Python"
    body = """
    <html>
      <body>
        <p>This is an <b>HTML</b> email sent from Python using the Gmail SMTP server.</p>
      </body>
    </html>
    """
    html_message = MIMEText(body, "html")
    html_message["Subject"] = subject
    html_message["From"] = sender_email
    html_message["To"] = recipient_email
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, html_message.as_string())
    server.quit()


def print_debug_env():
    print(sender_email)
    print(sender_password)
    print(ADMIN_EMAIL)


if __name__ == "__main__":
    # print_debug_env()
    localhost_send_email(
        "no-reply@example.com",
        "admin@example.com",
        "Breach",
        "A decoy password was used",
    )
