# email.py
import os, smtplib, ssl
import gblvar

def send_auth_code(receiver_email, channel_id):
    header = 'To:' + receiver_email + '\n' + 'From: ' + gblvar.email_address + '\n' + f'Subject:{gblvar.discord_guild_name} Discord Authentication Code\n'
    generated_hash = abs(hash(receiver_email)) % (10 ** 8)
    email_message = f"""
    Your authentication code is: {generated_hash}."""
    email_message = header + email_message

    f = open(f'.codes/{channel_id}.txt', "w+")
    f.write(str(generated_hash) + "\n" + receiver_email)
    f.close()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(gblvar.email_smtp_server, gblvar.email_port, context=context) as server:
        server.login(gblvar.email_address, gblvar.email_password)
        server.sendmail(gblvar.email_address, receiver_email, email_message)
        server.quit()
        print(f'📧 Email sent to {receiver_email}. Generated hash is {generated_hash}.')
