"""
This test can't easily be integrated into pytest because it requires the local aiosmtpd server to run.

python -m aiosmtpd -n -l localhost:1025

Also, if you want to test with MailSlurp, you have to reset the accounts for fresh credentials.

"""

from python_scripts.email_service import send_email

print("--- Starting LocalTest of email_service.py ---")
print("Using Local Dev Server: ")
# Send message that testUser has locked their account out after failing 3 times.
send_email(1, "testUser", using_mailslurp=False)

# Send message that someone has used hackedUser's decoy password.
send_email(2, "hackedUser", using_mailslurp=False)

print("Using MailSlurp: ")
# Same messages but this time using MailSlurp <https://app.mailslurp.com/inboxes/>
send_email(1, "testUser", using_mailslurp=True)
send_email(2, "hackedUser", using_mailslurp=True)
