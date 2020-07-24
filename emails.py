# email.py
import os, smtplib, ssl
import gblvar
from dotenv import load_dotenv

#EMAIL = os.getenv('EMAIL')
#PASSWORD = os.getenv('EMAIL_PASSWORD')
#EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
#EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
#DISCORD_NAME = os.getenv('DISCORD_NAME')

def send_auth_code(receiver_email, channel_id):
    header = 'To:' + receiver_email + '\n' + 'From: ' + gblvar.EMAIL + '\n' + f'Subject:{gblvar.DISCORD_NAME} Discord Authentication Code\n'
    generated_hash = abs(hash(receiver_email)) % (10 ** 8)
    email_message = f"""
    Your authentication code is: {generated_hash}."""
    email_message = header + email_message

    f = open(f'.codes/{channel_id}.txt', "w+")
    f.write(str(generated_hash) + "\n" + receiver_email)
    f.close()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(gblvar.EMAIL_SMTP_SERVER, gblvar.EMAIL_PORT, context=context) as server:
        server.login(gblvar.EMAIL, gblvar.PASSWORD)
        server.sendmail(gblvar.EMAIL, receiver_email, email_message)
        server.quit()
        print(f'📧 Email sent to {receiver_email}. Generated hash is {generated_hash}.')
