# envvar.py
import os
from dotenv import load_dotenv

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