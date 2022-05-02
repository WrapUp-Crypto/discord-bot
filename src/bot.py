import logging

import discord
from discord.ext import commands

from src.digests import Digests
from src.constants import BOT_TOKEN, BOT_PREFIX, LOGGING_FILE

logger = logging.getLogger("bot")


def configure_logging(logger):
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh = logging.FileHandler(filename=LOGGING_FILE)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


configure_logging(logger)
intents = discord.Intents(messages=True, guilds=True, emojis=True, reactions=True)

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}")


bot.add_cog(Digests(bot))
bot.run(BOT_TOKEN)
