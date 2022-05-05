import os

from dotenv import load_dotenv

load_dotenv()

BACKEND_API = os.getenv("BACKEND_API")
HEADERS = {"Backend-Api-Key": os.getenv("BACKEND_API_KEY")}
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PREFIX = os.getenv("BOT_PREFIX", default="wu?")

ICON_URL = os.getenv(
    "ICON_URL",
    default="https://aimages-videos.fra1.digitaloceanspaces.com/wrapUp/wrap%20up%20logo-03.png",
)

WRAPUP_HOME = "https://wrapup.ai"
WRAPUP_APP = "https://app.wrapup.ai"

LOGGING_DIR = os.getenv("LOGGING_DIR", default="./")

MIN_PERIOD = 1
MAX_PERIOD = 10

THEME_COLOR = 0xEC4899

DISCORD_INVITE = "https://discord.com/api/oauth2/authorize?client_id=921389404390576128&permissions=274878024768&scope=bot"
WRAPUP_DISCORD = "https://discord.com/invite/evKers3uCH"
