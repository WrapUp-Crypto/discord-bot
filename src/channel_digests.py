import discord
import aiohttp

from discord.ext import commands

from src.constants import HEADERS, ICON_URL, WRAPUP_APP, WRAPUP_HOME
from src.backend_api import (
    get_channel_top_reacted_messages,
    get_channel_most_replied_messages,
)
from src.exceptions import BackendAPIError


class Digests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def digest(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid `digest` command passed...")

    @digest.command(name="channel")
    @commands.guild_only()
    async def channel_digest(
        self, ctx, channel: discord.TextChannel = None, period: int = 1
    ):
        if period < 1 or period > 30:
            await ctx.send("Period must be in range `[1 - 30]`")
            return

        channel = channel or ctx.channel

        async with aiohttp.ClientSession(headers=HEADERS) as session:
            try:
                top_reacted = await get_channel_top_reacted_messages(
                    session=session,
                    server_id=ctx.guild.id,
                    channel_id=channel.id,
                    since_days=period,
                )
                most_replied = await get_channel_most_replied_messages(
                    session=session,
                    server_id=ctx.guild.id,
                    channel_id=channel.id,
                    since_days=period,
                )

            except BackendAPIError as e:
                print(e)
                await ctx.send("Failed to fetch data from WrapUp server :(")
                return

            embed = await self.format_digest(
                ctx=ctx,
                top_reacted=top_reacted,
                most_replied=most_replied,
                period=period,
                channel=channel,
            )

            await ctx.send(embed=embed)

    # Errors
    @channel_digest.error
    async def digest_error(self, ctx, error):
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send("Channel not found.")

        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("WrapUp can't be used in DMs")

        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send("Command not found.")

        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid command arguments.")

        print(type(error), error)

    async def format_message(self, ctx, message_id, max_words=15):
        message = await ctx.fetch_message(message_id)

        author = message.author.mention
        words = message.content.split(" ")
        if len(words) > max_words:
            content = " ".join(words[:max_words]) + "..."
        else:
            content = message.content

        return f"{author} - {content} - [View Message]({message.jump_url})"

    async def format_digest(self, ctx, channel, period, top_reacted, most_replied):
        embed = discord.Embed(colour=0xEC4899)
        day_str = "24h" if period == 1 else f"{period} days"
        embed.description = (
            f"{channel.mention} channel digest for the last __{day_str}.__"
        )

        invoked_parents = " ".join(ctx.invoked_parents)
        command = f"{ctx.prefix}{invoked_parents} {ctx.command.name}"
        embed.set_footer(text=f"Bot Invoked With '{command}'", icon_url=ICON_URL)

        if len(top_reacted) == 0:
            value = "No data.\n\u200B"
        else:
            value = []
            for i, msg in enumerate(top_reacted):
                formatted_msg = await self.format_message(
                    ctx=ctx, message_id=int(msg["message"]["native_id"])
                )
                value.append(
                    f"**{i+1}.** {formatted_msg} - `{int(msg['score'])} reacts`"
                )

            value = "\n---\n".join(value)
            value += "\n\u200B"

        embed.add_field(name="Top 3 Reacted Messages\n", inline=False, value=value)

        if len(most_replied) == 0:
            value = "No data.\n\u200B"
        else:
            value = []
            for i, msg in enumerate(most_replied):
                formatted_msg = await self.format_message(
                    ctx=ctx, message_id=int(msg["message"]["native_id"])
                )
                value.append(
                    f"**{i+1}.** {formatted_msg} - `{int(msg['n_replies'])} replies`"
                )

            value = "\n---\n".join(value)
            value += "\n\u200B"

        embed.add_field(name="Top 3 Most Replied Messages", inline=False, value=value)

        learn_more = (
            f"**[Full Digest]({WRAPUP_APP})** | "
            + f"**[Homepage]({WRAPUP_HOME})** | **Help** - `wu?help`"
        )
        embed.add_field(name="Learn More", inline=False, value=learn_more)

        return embed
