# main.py
import os, discord, random, re, smtplib, ssl
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

# .env variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_ID')
DISCORD_WELCOME_CHANNEL = os.getenv('DISCORD_WELCOME_CHANNEL')
PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL = os.getenv('EMAIL')
ALLOWED_EMAILS = os.getenv('ALLOWED_EMAILS').split(":")
DISCORD_ROLE = os.getenv('DISCORD_ROLE')
DISCORD_NAME = os.getenv('DISCORD_NAME')
EMAIL_FORMAT = os.getenv('EMAIL_FORMAT')
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))

client = discord.Client()



# MARK - When bot connects (use this to verify you are connected to the good server)
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.id == GUILD:
            break
        #elif guild.id != GUILD:
        #    print(f'⚠️ WARNING: Connected to unrecognized server named {guild.name}')

    print(f'🌐 {client.user} is connected to the following guild: {guild.name}(id: {guild.id})')

    #members = '\n - '.join([member.name for member in guild.members])
    #print(f'Guild Members:\n - {members}')



# MARK - When someone joins the Guild
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to the {DISCORD_NAME} Discord server! To verify your identity, please enter your {EMAIL_FORMAT} email address')



# MARK - When someone send a message
@client.event
async def on_message(message):

    # Check if message was sent by the bot
    if message.author == client.user:
        return

    # Check if the message was a DM
    if message.channel.type != discord.ChannelType.private:
        #print("This message was not sent on a private chat")
        return

    # Parses the string for a list of emails
    receiver_email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', message.content)


    # The message received is a code
    if message.content.isnumeric():
        try:
            f = open(f'.codes/{message.channel.id}', "r")
            data = f.readlines()
            user_email = data[1].strip()
            user_code = data[0].strip()
            f.close()

            if user_code == re.search(r'[\w\.-]+@[\w\.-]+\.\w+', ""):
                response = f'Please enter your {EMAIL_FORMAT} email address first.'
                await message.channel.send(response)

            elif user_email == re.search(r'[\w\.-]+@[\w\.-]+\.\w+', ""):
                response = f'Please enter your {EMAIL_FORMAT} email address first.'
                await message.channel.send(response)

            elif message.content == user_code:
                new_guild = client.get_guild(int(GUILD))

                member = new_guild.get_member(message.author.id)
                role = new_guild.get_role(int(DISCORD_ROLE))
                await member.add_roles(role)

                print(f'✅ The user {user_email} was added to the Discord')
                response = f'Welcome to {DISCORD_NAME}! You can now use the Discord Server.'
                await message.channel.send(response)

            else:
                print(f'Invalid code given for {user_email}')
                response = "The code given is invalid. Please try again."
                await message.channel.send(response)

        # File does not exist yet
        except FileNotFoundError:
            response = f'Please enter your {EMAIL_FORMAT} email address first.'
            await message.channel.send(response)


    # No email was given
    elif receiver_email == re.search(r'[\w\.-]+@[\w\.-]+\.\w+', ""):
        response = "Please enter a valid email address."
        await message.channel.send(response)


    # Email is in the list of valid emails
    elif receiver_email.group(0) in ALLOWED_EMAILS:
        #port = 465
        header = 'To:' + receiver_email.group(0) + '\n' + 'From: ' + EMAIL + '\n' + f'Subject:{DISCORD_NAME} Discord Authentication Code\n'
        generated_hash = abs(hash(receiver_email.group(0))) % (10 ** 8)

        email_message = f"""
        Your authentication code is: {generated_hash}."""
        email_message = header + email_message

        f = open(f'.codes/{message.channel.id}', "w+")
        f.write(str(generated_hash) + "\n" + receiver_email.group(0))
        f.close()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(EMAIL_SMTP_SERVER, EMAIL_PORT, context=context) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, receiver_email.group(0), email_message)
            server.quit()
            print(f'Email sent to {receiver_email.group(0)}. Generated hash is {generated_hash}.')

        response = f'An email was sent to {receiver_email.group(0)} with an authentication code. Please enter the code here.'
        await message.channel.send(response)


    # Email is not in the list of valid emails
    else:
        response = 'Sorry, that email is not in the list of allowed emails. Please contact the channel owner.'
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