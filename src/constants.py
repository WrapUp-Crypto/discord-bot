import os

from dotenv import load_dotenv

load_dotenv()

BACKEND_API = os.getenv("BACKEND_API")
HEADERS = {"Backend-Api-Key": os.getenv("BACKEND_API_KEY")}
BOT_TOKEN = os.getenv("BOT_TOKEN")

ICON_URL = (
    "https://aimages-videos.fra1.digitaloceanspaces.com/wrapUp/wrap%20up%20logo-03.png"
)

WRAPUP_HOME = "https://wrapup.ai"
WRAPUP_APP = "https://app.wrapup.ai"
