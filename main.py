# main.py
import os, discord, random, re
import emails
import gblvar
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

client = discord.Client()



# MARK - When bot connects
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.id == gblvar.GUILD:
            break

    print(f'🌐 {client.user} is connected to {guild.name} (id: {guild.id})')



# MARK - When someone joins the Guild
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to the {gblvar.DISCORD_NAME} Discord server! To verify your identity, please enter your {gblvar.EMAIL_FORMAT} email address')



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
            f = open(f'.codes/{message.channel.id}.txt', "r")
            data = f.readlines()
            user_email = data[1].strip()
            user_code = data[0].strip()
            f.close()

            if user_code == re.search(r'[\w\.-]+@[\w\.-]+\.\w+', ""):
                response = f'Please enter your {gblvar.EMAIL_FORMAT} email address first.'
                await message.channel.send(response)

            elif user_email == re.search(r'[\w\.-]+@[\w\.-]+\.\w+', ""):
                response = f'Please enter your {gblvar.EMAIL_FORMAT} email address first.'
                await message.channel.send(response)

            elif message.content == user_code:
                new_guild = client.get_guild(int(gblvar.GUILD))

                member = new_guild.get_member(message.author.id)
                role = new_guild.get_role(int(gblvar.DISCORD_ROLE))
                await member.add_roles(role)

                print(f'✅ The user {user_email} was added to the Discord')
                response = f'Welcome to {gblvar.DISCORD_NAME}! You can now use the Discord Server.'
                await message.channel.send(response)

            else:
                print(f'Invalid code given for {user_email}')
                response = "The code given is invalid. Please try again."
                await message.channel.send(response)

        # File does not exist yet
        except FileNotFoundError:
            response = f'Please enter your {gblvar.EMAIL_FORMAT} email address first.'
            await message.channel.send(response)


    # No email was given
    elif receiver_email == re.search(r'[\w\.-]+@[\w\.-]+\.\w+', ""):
        response = "Please enter a valid email address."
        await message.channel.send(response)


    # Email is in the list of valid emails
    elif receiver_email.group(0) in gblvar.ALLOWED_EMAILS:
        emails.send_auth_code(receiver_email.group(0), message.channel.id)
        response = f'An email was sent to {receiver_email.group(0)} with an authentication code. Please enter the code here.'
        await message.channel.send(response)


    # Email is not in the list of valid emails
    else:
        response = 'Sorry, that email is not in the list of allowed emails. Please contact the channel owner.'
        await message.channel.send(response)



# MARK - Take care of exceptions by displaying them in the terminal & saving them to a log file
@client.event
async def on_error(event, *args, **kwargs):
    error_description = str(event)
    for arg in args:
        error_description += "\n"
        error_description += str(arg)
    for kwarg in kwargs:
        error_description += "\n"
        error_description += str(kwarg)

    with open('err.log', 'a') as f:
        if event == 'on_message':
            error_description += "\n \n"
            f.write(f'Unhandled message: {error_description}')
        else:
            raise



client.run(gblvar.TOKEN)