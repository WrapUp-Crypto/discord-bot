from discord.ext import commands
import discord

from src.channel_digests import Digests
from src.constants import BOT_TOKEN


intents = discord.Intents(messages=True, guilds=True, emojis=True, reactions=True)

bot = commands.Bot(command_prefix="wu?", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


bot.add_cog(Digests(bot))
bot.run(BOT_TOKEN)
