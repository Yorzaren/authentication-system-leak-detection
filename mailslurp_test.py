"""
DONT USE

"""
"""
# TODO: FIX THIS

from dotenv import load_dotenv
load_dotenv()  # Load the secrets from the .env file

import os
# get an api key at https://app.mailslurp.com/sign-up
import mailslurp_client
from smtplib import SMTP
from mailslurp_client import CreateInboxDto

api_key = os.environ.get('MAILSLURP_API_KEY')

# create a mailslurp configuration
configuration = mailslurp_client.Configuration()
configuration.api_key['x-api-key'] = api_key


def test_can_send_with_smtp():
    with mailslurp_client.ApiClient(configuration) as api_client:
        inbox_controller = mailslurp_client.InboxControllerApi(api_client)
        inbox1 = inbox_controller.create_inbox_with_options(CreateInboxDto(inbox_type="SMTP_INBOX"))
        inbox2 = inbox_controller.create_inbox()
        assert "@mailslurp.mx" in inbox1.email_address

        # get smtp imap access
        smtp_access = inbox_controller.get_imap_smtp_access(inbox_id=inbox1.id)
        msg = "Subject: Test subject\r\n\r\nThis is the body"

        with SMTP(host=smtp_access.smtp_server_host, port=smtp_access.smtp_server_port) as smtp:
            smtp.login(user=smtp_access.smtp_username, password=smtp_access.smtp_password)
            smtp.sendmail(from_addr=inbox1.email_address, to_addrs=[inbox2.email_address], msg=msg)
            smtp.quit()

        wait_for_controller = mailslurp_client.WaitForControllerApi(api_client)
        email = wait_for_controller.wait_for_latest_email(inbox_id=inbox2.id)
        assert "Test subject" in email.subject

#test_can_send_with_smtp()
"""