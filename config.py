from os import getenv
from dotenv import load_dotenv

load_dotenv("config.env")

# connection
API_ID = int(getenv("API_ID", "")) 
API_HASH = getenv("API_HASH", "")
TOKEN = getenv("TOKEN", "")
STRING_SESSION = getenv("STRING_SESSION", "")
STRING_SESSION1 = getenv("STRING_SESSION1", "")
STRING_SESSION2 = getenv("STRING_SESSION2", "")
STRING_SESSION3 = getenv("STRING_SESSION3", "")
STRING_SESSION4 = getenv("STRING_SESSION4", "")

# other vars
DB_URL = getenv("DB_URL", "") # using postgressql
UBOT_LOG = int(getenv("UBOT_LOG") or 0)
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split(", ")))


# Heroku Vars
HEROKU_API_KEY = getenv("HEROKU_API_KEY", "")
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", "")
