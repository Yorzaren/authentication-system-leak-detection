"""

Basic python script to send emails

Google doesn't allow for us to use an account to send mails insecurely,
so we'll use mailslurp.com to generate test email accounts to send and receive
messages.

Also included is a localhost DebuggingServer

Mailslurp has a limit to how many emails can be sent and received so use it sparingly.

USAGE:

send_email(system_type, msg_type, account_name)

system_type: test | live
msg_type:
 - 1 for user account getting locked out
 - 2 for decoy password getting used
account_name: string

 """
import json  # To help read the mailslurp error message
import os  # Used to get the .env file
import smtplib
from email.mime.text import MIMEText
from smtplib import SMTP

import mailslurp_client
from dotenv import load_dotenv  # Used to load info from the .env file


def mailslurpt_send_email(subject_string, message_string):
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

    except AssertionError:
        print("Missing or incorrectly configured .env file")
    except mailslurp_client.ApiException as x:
        # The mailslurp_client.ApiException returns a body with json format
        # Read back the message to know which is the issue.
        print("Mailslurp variables are misconfigured.\n" + str(json.loads(x.body)["message"]))


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
    except Exception as e:
        print(e)
        print("Error: Cant send email\nIf using localhost run:\npython -m smtpd -c DebuggingServer -n localhost:1025")


def send_email(email_system, msg_type, account_name):
    email_title = "default title"
    message = "default message"

    if msg_type == 1:
        print("user account locked")
        email_title = f"[System] Account named {account_name} as been locked for suspicious activity"
        message = (
            f"Dear Admin,\nThe account named {account_name} has made 10 bad attempts to get into their account. "
            f"The system has locked {account_name}."
        )
    elif msg_type == 2:
        print("system breach")
        email_title = f"[ALERT] A decoy password has been used for {account_name}"
        message = (
            f"Dear Admin,\nA decoy password for user {account_name} has been used." f"The database might be breached."
        )

    if email_system == "test":
        # sender_email, recipient_email are made up because they don't really exist beyond the DebuggingServer
        localhost_send_email("no-reply@example.com", "admin@example.com", email_title, message)
    elif email_system == "live":
        # Use sparingly
        mailslurpt_send_email(email_title, message)
