from os import getenv
from dotenv import load_dotenv

load_dotenv("config.env")

# connection
API_ID = int(getenv("API_ID", "")) 
API_HASH = getenv("API_HASH", "")
STRING_SESSION = getenv("STRING_SESSION", "")
TOKEN = getenv("TOKEN", "")
# other vars
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split(", ")))
