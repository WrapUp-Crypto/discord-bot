import logging

import aiohttp

import discord
from discord.ext import commands

from src.constants import (
    HEADERS,
    ICON_URL,
    THEME_COLOR,
    WRAPUP_APP,
    WRAPUP_HOME,
    BOT_PREFIX,
    MIN_PERIOD,
    MAX_PERIOD,
    WRAPUP_DISCORD,
)
from src.backend_api import (
    get_channel_top_reacted_messages,
    get_channel_most_replied_messages,
    get_server_most_replied_messages,
    get_server_top_reacted_messages,
    get_emerging_channels,
    get_busiest_channels,
    get_server_pinned_messages,
    get_channel_active_users,
)
from src.exceptions import BackendAPIError


logger = logging.getLogger("bot")


class Digests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        help="Group of sub-commands that generate digests.", aliases=["d", "dg", "dig"]
    )
    async def digest(self, ctx):
        if ctx.invoked_subcommand is None:
            msg = "Invalid `digest` sub-command passed."
            logger.warning(msg)
            await ctx.send(msg)

    @digest.command(
        name="channel",
        help="Generate a channel digest for a selected channel.",
        aliases=["c", "chn"],
    )
    @commands.guild_only()
    @commands.max_concurrency(number=25, wait=True, per=commands.BucketType.guild)
    @commands.cooldown(rate=5, per=60, type=commands.BucketType.channel)
    async def channel_digest(
        self, ctx, channel: discord.TextChannel = None, period: int = 1
    ):
        if period < MIN_PERIOD or period > MAX_PERIOD:
            msg = (
                f"Period must be in range `[{MIN_PERIOD} - {MAX_PERIOD}]`. "
                + "You can select longer periods in the WrapUp web dashboard."
            )
            logger.warning(msg)
            await ctx.send(msg)
            return

        channel = channel or ctx.channel

        top_n_results = 4
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            try:
                top_reacted = await get_channel_top_reacted_messages(
                    session=session,
                    server_id=ctx.guild.id,
                    channel_id=channel.id,
                    since_days=period,
                    limit=top_n_results,
                )
                most_replied = await get_channel_most_replied_messages(
                    session=session,
                    server_id=ctx.guild.id,
                    channel_id=channel.id,
                    since_days=period,
                    limit=top_n_results,
                )
                active_users = await get_channel_active_users(
                    session=session,
                    server_id=ctx.guild.id,
                    channel_id=channel.id,
                    since_days=period,
                    limit=5,
                )

            except BackendAPIError:
                await ctx.send(
                    "Couldn't fetch data from WrapUp server ????. Please try again later."
                )
                return
            except aiohttp.ClientConnectorError as e:
                msg = f"Couldn't connect to WrapUp backend: {e}"
                logger.error(msg)
                await ctx.send("Couldn't connect to WrapUp server ????")
                return

            day_str = "24h" if period == 1 else f"{period} days"
            embed = await self.format_digest(
                ctx=ctx,
                description=f"{channel.mention} channel digest for the __last {day_str}.__",
                top_reacted=top_reacted,
                most_replied=most_replied,
                active_users=active_users,
                top_n=top_n_results,
                title="Channel Digest",
            )

            await ctx.send(embed=embed)

    @digest.command(
        name="server",
        help="Generate a server digest for the current server.",
        aliases=["s", "srv", "srvr"],
    )
    @commands.guild_only()
    @commands.max_concurrency(number=25, wait=True, per=commands.BucketType.guild)
    @commands.cooldown(rate=5, per=60, type=commands.BucketType.channel)
    async def server_digest(self, ctx, period: int = 1):
        if period < MIN_PERIOD or period > MAX_PERIOD:
            msg = (
                f"Period must be in range `[{MIN_PERIOD} - {MAX_PERIOD}]`. "
                + "You can select longer periods in the WrapUp web dashboard."
            )
            logger.warning(msg)
            await ctx.send(msg)
            return

        async with aiohttp.ClientSession(headers=HEADERS) as session:
            try:
                top_reacted = await get_server_top_reacted_messages(
                    session=session,
                    server_id=ctx.guild.id,
                    since_days=period,
                    limit=3,
                )
                most_replied = await get_server_most_replied_messages(
                    session=session,
                    server_id=ctx.guild.id,
                    since_days=period,
                    limit=3,
                )
                emerging_channels = await get_emerging_channels(
                    session=session,
                    server_id=ctx.guild.id,
                    since_days=period,
                    limit=3,
                )
                busiest_channels = await get_busiest_channels(
                    session=session,
                    server_id=ctx.guild.id,
                    since_days=period,
                    limit=3,
                )
                pinned_messages = await get_server_pinned_messages(
                    session=session,
                    server_id=ctx.guild.id,
                    since_days=period,
                    limit=3,
                )

            except BackendAPIError:
                await ctx.send(
                    "Couldn't fetch data from WrapUp server ????. Please try again later."
                )
                return

            except aiohttp.ClientConnectorError as e:
                msg = f"Couldn't connect to WrapUp backend: {e}"
                logger.error(msg)
                await ctx.send("Couldn't connect to WrapUp server ????")
                return

            day_str = "24h" if period == 1 else f"{period} days"
            embed = await self.format_digest(
                ctx=ctx,
                description=f"**{ctx.guild.name}** server digest for the __last {day_str}.__",
                top_reacted=top_reacted,
                most_replied=most_replied,
                top_n=3,
                emerging_channels=emerging_channels,
                busiest_channels=busiest_channels,
                pinned_messages=pinned_messages,
                title="Server Digest",
            )

            await ctx.send(embed=embed)

    @channel_digest.error
    @server_digest.error
    async def digest_error(self, ctx, error):
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send("Channel not found.")

        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("WrapUp can't be used in DMs")

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(
                f"Command not found. Use `{BOT_PREFIX}help` to see available commands."
            )

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                "Bot called too frequently. Please wait a minute before calling it again."
            )

        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                "Invalid command arguments. "
                + f"Use `{BOT_PREFIX}help` to see available command arguments."
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This WrapUp command cannot be called in DMs.")
        else:
            await ctx.send("Something went wrong ????. Our devs are working on it!")

    @staticmethod
    def format_message(
        msg, author_id, server_id, channel_id, message_id, max_chars=13 * 7
    ):
        jump_url = f"https://discord.com/channels/{server_id}/{channel_id}/{message_id}"
        author = f"<@{author_id}>"
        msg_decoded = msg.encode("utf-8", "ignore")

        if len(msg_decoded) > max_chars:
            # Maximum discord embed field value can be 1024 chars, so we cut each message
            # with respect to its original encoding

            # Find index for the space character that is closest to max_chars, but less or equal to
            # max_chars
            space_indexes = [
                i for i, x in enumerate(msg_decoded[:max_chars]) if x == " "
            ]

            if len(space_indexes) == 0:
                # No spaces found.
                cutoff_index = max_chars
            else:
                cutoff_index = space_indexes[-1]

            content_decoded = msg_decoded[:cutoff_index].decode("utf-8", "ignore")
            content = f"{content_decoded}..."
        else:
            content = msg

        return f"{author} ??? {content} ??? [View Message]({jump_url})"

    async def format_emerging_channel(self, channel_id, score):
        try:
            channel = await self.bot.fetch_channel(channel_id)
        except Exception as e:
            logger.error(e)
            return "__Unknown Channel__"

        if score < 0.1:
            score_str = f"+{score * 100:.2f}%"
        elif score < 1:
            score_str = f"+{score * 100:.1f}%"
        else:
            score_str = f"+{score * 100:.0f}%"

        return f"{channel.mention} ??? `{score_str}`"

    async def format_busiest_channel(self, channel_id, n_msgs):
        try:
            channel = await self.bot.fetch_channel(channel_id)
        except Exception as e:
            logger.error(e)
            return "__Unknown Channel__"

        return f"{channel.mention} ??? `{n_msgs}` human messages sent"

    async def format_digest(
        self,
        ctx,
        description,
        top_reacted,
        most_replied,
        emerging_channels=None,
        busiest_channels=None,
        pinned_messages=None,
        active_users=None,
        title=None,
        top_n=5,
    ):
        embed = discord.Embed(colour=THEME_COLOR)
        embed.description = (
            f"{description}\nSee all commands with `{BOT_PREFIX}help`\n\u200B"
        )

        if title is not None:
            embed.title = title

        invoked_parents = " ".join(ctx.invoked_parents)
        command = f"{ctx.prefix}{invoked_parents} {ctx.command.name}"
        embed.set_footer(text=f"Bot Called With {command}", icon_url=ICON_URL)

        # Most reacted messages
        if len(top_reacted) == 0:
            value = "No messages found.\n\u200B"
        else:
            value = []
            for i, msg in enumerate(top_reacted):
                formatted_msg = self.format_message(
                    server_id=ctx.guild.id,
                    channel_id=msg["message"]["channel"],
                    message_id=msg["message"]["native_id"],
                    author_id=msg["message"]["author"]["native_id"],
                    msg=msg["message"]["raw_text"],
                )
                value.append(
                    f"**{i+1}.** {formatted_msg} (`{int(msg['score'])} reacts`)"
                )

            value = "\n".join(value)
            value += "\n\u200B"

        embed.add_field(
            name=f"Top {top_n} Reacted Messages\n", inline=False, value=value
        )

        # Most replied messages
        if len(most_replied) == 0:
            value = "No messages found.\n\u200B"
        else:
            value = []
            for i, msg in enumerate(most_replied):
                formatted_msg = self.format_message(
                    server_id=ctx.guild.id,
                    channel_id=msg["message"]["channel"],
                    message_id=msg["message"]["native_id"],
                    author_id=msg["message"]["author"]["native_id"],
                    msg=msg["message"]["raw_text"],
                )
                value.append(
                    f"**{i+1}.** {formatted_msg} (`{int(msg['n_replies'])} replies`)"
                )

            value = "\n".join(value)
            value += "\n\u200B"
        embed.add_field(
            name=f"Top {top_n} Most Replied Messages", inline=False, value=value
        )

        # Pinned messages
        if pinned_messages is not None:
            if len(pinned_messages) == 0:
                value = "No messages found.\n\u200B"
            else:
                value = []
                for i, msg in enumerate(pinned_messages):
                    formatted_msg = self.format_message(
                        server_id=ctx.guild.id,
                        channel_id=msg["channel"],
                        message_id=msg["native_id"],
                        author_id=msg["author"]["native_id"],
                        msg=msg["raw_text"],
                    )
                    value.append(f"**{i+1}.** {formatted_msg}")

                value = "\n".join(value)
                value += "\n\u200B"

            embed.add_field(
                name="3 Newest Pinned Messages",
                inline=False,
                value=value,
            )

        # Emerging channels
        if emerging_channels is not None:
            if len(emerging_channels) == 0:
                value = "No emerging channels found.\n\u200B"
            else:
                value = []
                for i, chn in enumerate(emerging_channels):
                    formatted_msg = await self.format_emerging_channel(
                        channel_id=int(chn["native_id"]), score=chn["growth_ratio"]
                    )
                    value.append(f"**{i+1}.** {formatted_msg}")

                value = "\n".join(value)
                value += "\n\u200B"

            embed.add_field(
                name="Top 3 Emerging Channels (largest increase of sent messages)",
                inline=False,
                value=value,
            )

        # Busiest channels
        if busiest_channels is not None:
            if len(busiest_channels) == 0:
                value = "No active channels found.\n\u200B"
            else:
                value = []
                for i, chn in enumerate(busiest_channels):
                    formatted_msg = await self.format_busiest_channel(
                        channel_id=int(chn["native_id"]), n_msgs=chn["n_messages"]
                    )
                    value.append(f"**{i+1}.** {formatted_msg}")

                value = "\n".join(value)
                value += "\n\u200B"

            embed.add_field(
                name="Top 3 Most Busiest Channels",
                inline=False,
                value=value,
            )

        # Most active users
        if active_users is not None:
            if len(active_users) == 0:
                value = "No active users found.\n\u200B"
            else:
                value = []
                for i, usr in enumerate(active_users):
                    user_mention = f"<@{usr['id']}>"
                    formatted_msg = None
                    value.append(
                        f"**{i+1}.** {user_mention} ??? `{usr['n_messages']}` messages"
                    )

                value = "\n".join(value)
                value += "\n\u200B"

            embed.add_field(
                name="Top 5 Most Active Members",
                inline=False,
                value=value,
            )

        learn_more = (
            f"**[Full Digest]({WRAPUP_APP})** | "
            + f"**[About WrapUp]({WRAPUP_HOME})** | "
            + f"**[Support]({WRAPUP_DISCORD})**"
        )
        embed.add_field(name="Learn More", inline=False, value=learn_more)

        return embed

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        logger.error(error)
