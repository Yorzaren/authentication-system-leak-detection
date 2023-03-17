"""

Basic python script to send emails

Google doesn't allow for us to use an account to send mails insecurely,
so we'll use MailSlurp.com to generate test email accounts to send and receive
messages.

Also included is a localhost aiosmtpd server

MailSlurp has a limit to how many emails can be sent and received so use it sparingly.

USAGE:

send_email(msg_type, account_name, using_mailslurp)

using_mailslurp:
 - False (default)
 - True

msg_type:
 - 1 for user account getting locked out
 - 2 for decoy password getting used
 - 3 for a locked account being attempted multiple times
 - 4 for when the system has more than one decoy password used across users
account_name: string

 """
import json  # To help read the mailslurp error message
import os  # Used to get the .env file
import smtplib
from email.mime.text import MIMEText
from smtplib import SMTP

import mailslurp_client
from dotenv import load_dotenv  # Used to load info from the .env file


def __mailslurp_send_email(subject_string: str, message_string: str):
    try:
        load_dotenv()  # Load the secrets from the .env file
        api_key = os.environ.get("MAILSLURP_API_KEY")
        sender_id = os.environ.get("MAILSLURP_SENDER_EMAIL_ID")
        receiver_id = os.environ.get("MAILSLURP_RECIEVER_EMAIL_ID")

        # Check for the keys
        assert "MAILSLURP_API_KEY" in os.environ
        assert "MAILSLURP_SENDER_EMAIL_ID" in os.environ
        assert "MAILSLURP_RECIEVER_EMAIL_ID" in os.environ

        # create a mailslurp configuration
        configuration = mailslurp_client.Configuration()
        configuration.api_key["x-api-key"] = api_key

        with mailslurp_client.ApiClient(configuration) as api_client:
            # create an SMTP inbox
            inbox_controller = mailslurp_client.InboxControllerApi(api_client)
            system_email = inbox_controller.get_inbox(sender_id)
            admin_email = inbox_controller.get_inbox(receiver_id)
            # print(system_email)
            # print(admin_email)

            # get smtp imap access
            smtp_access = inbox_controller.get_imap_smtp_access(inbox_id=system_email.id)
            msg = "Subject: " + subject_string + "\r\n\r\n" + message_string

            with SMTP(host=smtp_access.smtp_server_host, port=smtp_access.smtp_server_port) as smtp:
                smtp.login(user=smtp_access.smtp_username, password=smtp_access.smtp_password)
                smtp.sendmail(from_addr=system_email.email_address, to_addrs=[admin_email.email_address], msg=msg)
                smtp.quit()
            print("Successfully sent email using MailSlurp")
    except AssertionError:
        print("Missing or incorrectly configured .env file")
    except mailslurp_client.ApiException as x:
        # The mailslurp_client.ApiException returns a body with json format
        # Read back the message to know which is the issue.
        print("MailSlurp variables are misconfigured.\n" + str(json.loads(x.body)["message"]))


# Requires you to use commandline to open the port
# python -m aiosmtpd -n -l localhost:1025
def __localhost_send_email(sender_email: str, recipient_email: str, email_subject: str, email_body: str):
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
            print("Successfully sent email using the local aiosmtpd server")
    except Exception as e:
        print(e)
        print("Error: Cant send email\nIf using localhost run:\npython -m aiosmtpd -n -l localhost:1025")


def send_email(msg_type: int, account_name: str, using_mailslurp=False):
    email_title = "default title"
    message = "default message"

    if msg_type == 1:
        print(f"Mail system has received notice: User Account Locked for {account_name}")
        email_title = f"[System] Account named {account_name} as been locked for suspicious activity"
        message = (
            f"Dear Admin,\nThe account named {account_name} has made 3 bad attempts to get into their account. "
            f"The system has locked {account_name}."
        )
    elif msg_type == 2:
        print("Mail system has received notice: System Breach")
        email_title = f"[IMPORTANT ALERT] A decoy password has been used for {account_name}"
        message = (
            f"Dear Admin,\nA decoy password for user {account_name} has been used. The database might be breached. "
            f"You should take action to lock the system."
        )
    elif msg_type == 3:
        print(f"Mail system has received notice: Continued Bad Login Attempts from {account_name}")
        email_title = f"[System] Account named {account_name} continues their bad login attempts"
        message = (
            f"Dear Admin,\nThe account named {account_name} continues their attempt to get into the locked account."
            f"No action necessary. However, you should continue to watch for suspicious activity across the system."
        )
    elif msg_type == 4:
        print("Mail system has received notice: System Breach")
        email_title = f"[VERY IMPORTANT ALERT] More than one account had their decoy password used"
        message = (
            f"Dear Admin,\nMultiple decoy passwords across they system has been used. The system has auto-locked every "
            f"account including the admin accounts."
        )
    if using_mailslurp is True:
        # Use sparingly
        __mailslurp_send_email(email_title, message)
    else:
        # sender_email, recipient_email are made up because they don't really exist beyond the local aiosmtpd server
        __localhost_send_email("no-reply@example.com", "admin@example.com", email_title, message)
