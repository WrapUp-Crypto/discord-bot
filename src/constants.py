import os

from dotenv import load_dotenv

load_dotenv()

BACKEND_API = os.getenv("BACKEND_API")
HEADERS = {"Backend-Api-Key": os.getenv("BACKEND_API_KEY")}
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PREFIX = os.getenv("BOT_PREFIX", default="wu?")

ICON_URL = (
    "https://aimages-videos.fra1.digitaloceanspaces.com/wrapUp/wrap%20up%20logo-03.png"
)

WRAPUP_HOME = "https://wrapup.ai"
WRAPUP_APP = "https://app.wrapup.ai"

LOGGING_FILE = os.getenv("LOGGING_FILE", default="./bot.log")
