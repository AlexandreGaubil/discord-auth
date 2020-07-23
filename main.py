# bot.py
import os, discord, random, re, smtplib, ssl
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_ID')
DISCORD_WELCOME_CHANNEL = os.getenv('DISCORD_WELCOME_CHANNEL')
PASSWORD = os.getenv('GMAIL_PASSWORD')
EMAIL = os.getenv('EMAIL')
ALLOWED_EMAILS = os.getenv('ALLOWED_EMAILS').split(":")

client = discord.Client()



# MARK - When bot connects (use this to verify you are connected to the good server)
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.id == GUILD:
            break
        elif guild.id != GUILD:
            print(f'⚠️ WARNING: Connected to unrecognized server named {guild.name}')

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')



# MARK - When someone joins the Guild
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Han House Discord server! To verify your identity, please enter your @uchicago.edu email address'
    )



# MARK - When someone send a message
@client.event
async def on_message(message):

    # Check if message was sent by the bot
    if message.author == client.user:
        return

    # Check if the message was a DM
    if message.channel.type != discord.ChannelType.private:
        print("This message was not sent on a private chat")
        return

    # Parses the string for a list of emails
    receiver_email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', message.content)


    # The message received is a code
    if message.content.isnumeric():
        f = open(f'.codes/{message.channel.id}', "r")

        user_email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', f.read())
        user_code = re.search(r'^[0-9]{8}$', f.read())

        if abs(hash(user_email)) % (10 ** 8) == user_code:
            member = message.author

            role = get(member.guild.roles, name="Member")
            await member.add_roles(role)

            response = "Welcome to Han House! You can now use the Discord Server."
            await message.channel.send(response)
            print("Numerical found")


    # No email was given
    elif receiver_email == re.search(r'[\w\.-]+@[\w\.-]+\.\w+', ""):
        response = "Please enter a valid email address. Contact gaubil@uchicago.edu if you are experiencing problems."
        await message.channel.send(response)


    # Email is in the list of valid emails
    elif receiver_email.group(0) in ALLOWED_EMAILS:
        port = 465
        header = 'To:' + receiver_email + '\n' + 'From: ' + EMAIL + '\n' + 'Subject:Han House Discord Authentication Code\n'
        generated_hash = abs(hash(receiver_email)) % (10 ** 8)

        email_message = f"""
        Your authentication code is: {generated_hash}."""
        email_message = header + email_message

        f = open(f'.codes/{message.channel.id}', "w")
        f.write(generated_hash)
        f.close()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, receiver_email, email_message)
            server.quit()
            print(f'Email sent to {receiver_email}. Generated hash is {generated_hash}.')

        response = f'An email was sent to {receiver_email} with an authentication code. Please enter the code here.'
        await message.channel.send(response)


    # Email is not in the list of valid emails
    else:
        response = "Sorry, that email is not in the list of allowed emails. Please contact gaubil@uchicago.edu if you are part of Han House."
        await message.channel.send(response)





# MARK - Take care of exceptions
#@client.event
#async def on_error(event, *args, **kwargs):
#    with open('err.log', 'a') as f:
#        if event == 'on_message':
#            f.write(f'Unhandled message: {args[0]}\n')
#        else:
#            raise

client.run(TOKEN)