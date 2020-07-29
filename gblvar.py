# envvar.py
import os, json
from dotenv import load_dotenv

with open('authorized_users.json') as f:
  authorized_users_data = json.load(f)

# ----- Authorized users -----
authorized_users = authorized_users_data['authorized_users']

with open('setup_info.json') as f:
    setup_info_data = json.load(f)

# ----- Discord information -----
discord_bot_token = setup_info_data['discord_bot_token']
discord_guild_id = setup_info_data['discord_guild_id']
discord_guild_name = setup_info_data['discord_guild_name']
discord_welcome_channel_id = setup_info_data['discord_welcome_channel_id']
discord_role_to_assign_id = setup_info_data['discord_role_to_assign_id']

# ----- Email information -----
email_password = setup_info_data['email_password']
email_address = setup_info_data['email_address']
email_smtp_server = setup_info_data['email_smtp_server']
email_port = setup_info_data['email_port']

# ----- Message customization -----
# A small string to specify what kind of email address should be used
email_type_specifier = setup_info_data['email_type_specifier']
# Number of digits in the code sent to the user
number_of_digits_hash = int(setup_info_data['number_of_digits_hash'])