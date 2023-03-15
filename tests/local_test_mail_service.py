"""
This test can't easily be integrated into pytest because it requires DebuggingServer to run.

python -m smtpd -c DebuggingServer -n localhost:1025

Also, if you want to test with mailslurp, you have to reset the accounts for fresh credentials.

"""
from python_scripts.email_service import send_email

print("--- Starting LocalTest of email_service.py ---")
print("Using DebuggingServer: ")
# Send message that testUser has locked their account out after failing 3 times.
send_email(1, "testUser", using_mailslurp=False)

# Send message that someone has used hackedUser's decoy password.
send_email(2, "hackedUser", using_mailslurp=False)

print("Using Mailslurp: ")
# Same messages but this time using Mailslurp <https://app.mailslurp.com/inboxes/>
send_email(1, "testUser", using_mailslurp=True)
send_email(2, "hackedUser", using_mailslurp=True)
