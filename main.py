# main.py
import os, discord, random, re
import emails
import gblvar
from discord.ext import commands
from discord.utils import get

client = discord.Client()



# MARK - When bot connects
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.id == gblvar.discord_guild_id:
            break

    print(f'🌐 {client.user} is connected to {guild.name} (id: {guild.id})')



# MARK - When someone joins the Guild
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to the {gblvar.discord_guild_name} Discord server! To verify your identity, please enter your {gblvar.email_type_specifier} email address')



# MARK - When someone send a message
@client.event
async def on_message(message):

    # Check if message was sent by the bot
    if message.author == client.user:
        return

    # Check if the message was a DM
    if message.channel.type != discord.ChannelType.private:
        return

    # Parses the message for a list of emails
    receiver_email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', message.content)
    no_regression_result = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', "")


    # The message received is a code
    if message.content.isnumeric():
        try:
            f = open(f'.codes/{message.channel.id}.txt', "r")
            data = f.readlines()
            user_email = data[1].strip()
            user_code = data[0].strip()
            f.close()

            if user_code == no_regression_result:
                response = f'Please enter your {gblvar.email_type_specifier} email address first.'
                await message.channel.send(response)

            elif user_email == no_regression_result:
                response = f'Please enter your {gblvar.email_type_specifier} email address first.'
                await message.channel.send(response)

            elif message.content == user_code:
                new_guild = client.get_guild(int(gblvar.discord_guild_id))
                member = new_guild.get_member(message.author.id)
                roles_to_add = []

                print(gblvar.authorized_users)

                for role_to_add in gblvar.authorized_users[user_email]:
                    roles_to_add.append(new_guild.get_role(int(role_to_add)))
                    role = new_guild.get_role(int(role_to_add))
                    await member.add_roles(role, reason="Discord Auth Bot")
                if roles_to_add == []:
                    role = new_guild.get_role(int(gblvar.discord_role_to_assign_id))
                    await member.add_roles(role, reason="Discord Auth Bot")

                print(f'✅ The user {user_email} was added to the Discord')
                response = f'Welcome to {gblvar.discord_guild_name}! You can now use the Discord Server.'
                await message.channel.send(response)

            else:
                print(f'Invalid code given for {user_email}')
                response = "The code given is invalid. Please try again."
                await message.channel.send(response)

        # File does not exist yet
        except FileNotFoundError:
            response = f'Please enter your {gblvar.email_type_specifier} email address first.'
            await message.channel.send(response)


    # No email was given
    elif receiver_email == no_regression_result:
        response = "Please enter a valid email address."
        await message.channel.send(response)


    # Email is in the list of valid emails
    elif receiver_email.group(0) in list(gblvar.authorized_users.keys()):
        emails.send_auth_code(receiver_email.group(0), message.channel.id)
        response = f'An email was sent to {receiver_email.group(0)} with an authentication code. Please enter the code here.'
        await message.channel.send(response)


    # Email is not in the list of valid emails
    else:
        response = 'Sorry, that email is not in the list of allowed emails. Please contact the channel owner.'
        await message.channel.send(response)



# MARK - Take care of exceptions by displaying them in the terminal & saving them to a log file
#@client.event
#async def on_error(event, *args, **kwargs):
#    error_description = str(event)
#    for arg in args:
#        error_description += "\n"
#        error_description += str(arg)
#    for kwarg in kwargs:
#        error_description += "\n"
#        error_description += str(kwarg)
#
#    with open('err.log', 'a') as f:
#        if event == 'on_message':
#            error_description += "\n \n"
#            f.write(f'Unhandled message: {error_description}')
#        else:
#            raise



client.run(gblvar.discord_bot_token)