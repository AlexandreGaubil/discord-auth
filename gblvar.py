# envvar.py
import os, json
from dotenv import load_dotenv

with open('json/authorized_users.json') as f:
  authorized_users_data = json.load(f)

# ----- Authorized users -----
authorized_users = authorized_users_data['authorized_users']

#with open('json/setup_info.json') as f:
#    setup_info_data = json.load(f)

# ----- Discord information -----
discord_bot_token = os.getenv('DISCORD_BOT_TOKEN') #setup_info_data['discord_bot_token']
discord_guild_id = int(os.getenv('DISCORD_GUILD_ID')) #setup_info_data['discord_guild_id']
discord_guild_name = os.getenv('DISCORD_GUILD_NAME') #setup_info_data['discord_guild_name']
discord_welcome_channel_id = int(os.getenv('DISCORD_WELCOME_CHANNEL_ID')) #setup_info_data['discord_welcome_channel_id']
discord_role_to_assign_id = int(os.getenv('DISCORD_ROLE_TO_ASSIGN_ID')) #setup_info_data['discord_role_to_assign_id']

# ----- Email information -----
email_password = os.getenv('EMAIL_PASSWORD') #setup_info_data['email_password']
email_address = os.getenv('EMAIL_ADDRESS') #setup_info_data['email_address']
email_smtp_server = os.getenv('EMAIL_SMTP_SERVER') #setup_info_data['email_smtp_server']
email_port = int(os.getenv('EMAIL_PORT')) #setup_info_data['email_port']

# ----- Message customization -----
# A small string to specify what kind of email address should be used
email_type_specifier = os.getenv('EMAIL_TYPE_SPECIFIER') #setup_info_data['email_type_specifier']
# Number of digits in the code sent to the user
number_of_digits_hash =  int(os.getenv('NUMBER_OF_DIGITS_HASH')) #int(setup_info_data['number_of_digits_hash'])