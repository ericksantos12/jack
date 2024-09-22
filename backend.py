import sys
import discord
import logging
from discord.ext import commands
from colorlog import ColoredFormatter
from dotenv import load_dotenv
import os

intents = discord.Intents.default()

# Initializing the logger
def colorlogger(name: str = 'my-discord-bot') -> logging.Logger:
    logger = logging.getLogger(name)
    stream = logging.StreamHandler()

    stream.setFormatter(ColoredFormatter("%(reset)s%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s"))
    logger.addHandler(stream)
    return logger  # Return the logger

log = colorlogger()

# Load environment variables from .env file
load_dotenv(dotenv_path='.env')

try:
    # Getting the variables
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    presence = os.getenv('PRESENCE', 'Bot is running!')

    discord_token = os.getenv('DISCORD_TOKEN')
    if discord_token is None:
        log.critical("DISCORD_TOKEN is not set in the .env file.")
        sys.exit()

    embed_url = os.getenv('EMBED_URL', '')
    
    igdb_client_id = os.getenv('IGDB_CLIENT_ID')
    igdb_client_secret = os.getenv('IGDB_CLIENT_SECRET')
    
    if igdb_client_id is None or igdb_client_secret is None:
        log.critical("IGDB_CLIENT_ID or IGDB_CLIENT_SECRET is not set in the .env file.")
        sys.exit()

except Exception as err:
    log.critical("Error getting variables from the .env file. Error: " + str(err))
    sys.exit()

# Set the logger's log level to the one in the config file
if log_level.upper().strip() in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    log.setLevel(log_level.upper().strip())
else:
    log.setLevel("INFO")
    log.warning(f"Invalid log level `{log_level.upper().strip()}`. Defaulting to INFO.")

# Initializing the client
client = commands.Bot(intents=intents)

def error_template(description: str) -> discord.Embed:
    _error_template = discord.Embed(
        title="Error!",
        description=description,
        color=0xff0000,
        url=embed_url
    )

    return _error_template.copy()

# Add your own functions and variables here
# Happy coding! :D
