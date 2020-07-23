# bot.py
import os, discord, random, re, smtplib, ssl
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_ID')
PASSWORD = os.getenv('GMAIL_PASSWORD')
EMAIL = os.getenv('EMAIL')
ALLOWED_EMAILS = os.getenv('ALLOWED_EMAILS').split(":")

client = discord.Client()



# When bot connects (use this to verify you are connected to the good server)
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



# When someone joins the Guild
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Han House Discord server! To verify your identity, please enter your @uchicago.edu email address'
    )



# When someone send a message
@client.event
async def on_message(message):

    # Check if message was sent by the bot
    if message.author == client.user:
        return

    #print(message.content)
    #print(message.channel.type)
    #print(ALLOWED_EMAILS)

    receiver_email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', message.content)

    if receiver_email == re.search(r'[\w\.-]+@[\w\.-]+\.\w+', ""):
        response = "Please enter a valid email address. Contact gaubil@uchicago.edu if this is not working and the email is valid."
        await message.channel.send(response)

    elif receiver_email.group(0) in ALLOWED_EMAILS:
        member = message.author
        print(member.roles)

        # for guild in client.guilds:
        #     if guild.id == GUILD:
        #         break

        role = get(member.guild.roles, name="Member")
        # try:
        #     await user.add_roles(discord.utils.get(member, name=role)) #add the role
        # except Exception as e:
        #     await print('There was an error running this command ' + str(e)) #if error
        # else:
        #     await print("""Verified: {}""".format(user)) # no errors, say verified
        await member.add_roles(role)
        #await client.add_roles(member, role)

        response = "Welcome to Han House! You can now use the Discord Server."
        await message.channel.send(response)

        #port = 465  # For SSL
        # header = 'To:' + receiver_email + '\n' + 'From: ' + EMAIL + '\n' + 'Subject:Han House Discord Authentication Code\n'
        # print(receiver_email)
        # generated_hash = abs(hash(receiver_email)) % (10 ** 8)

        # email_message = f"""
        # Your authentication code is: {generated_hash}."""
        # email_message = header + email_message

        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        #     server.login(EMAIL, PASSWORD)
        #     server.sendmail(EMAIL, receiver_email, email_message)
        #     server.quit()
        #     print(f'Email sent to {receiver_email}. Generated hash is {generated_hash}.')
        # response = f'An email was sent to {receiver_email} with an authentication code. Please enter the code here.'
        # await message.channel.send(response)

    else:
        response = "Sorry, that email is not in the list of allowed emails. Please contact gaubil@uchicago.edu if you are part of Han House."
        await message.channel.send(response)

    # if message.channel.type == 'private':
    #     print("Private message sent")
    #     answers = [
    #         "Welcome! This won't be long"
    #     ]
    #     if message.content == '99!':
    #         response = random.choice(answers)
    #         await message.channel.send(response)
    # else:
    #     print("Not a private chat")



# Take care of exceptions
#@client.event
#async def on_error(event, *args, **kwargs):
#    with open('err.log', 'a') as f:
#        if event == 'on_message':
#            f.write(f'Unhandled message: {args[0]}\n')
#        else:
#            raise

client.run(TOKEN)