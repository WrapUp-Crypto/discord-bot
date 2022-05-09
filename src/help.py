import discord
from discord.ext import commands

from src.constants import (
    BOT_PREFIX,
    DISCORD_INVITE,
    ICON_URL,
    THEME_COLOR,
    WRAPUP_HOME,
    WRAPUP_DISCORD,
)


class Help(commands.Cog):
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(colour=THEME_COLOR)

        embed.title = "WrapUp Help"
        embed.description = (
            f"Prefix for this server is `{BOT_PREFIX}`\n"
            + f"To find out more about a command, type `{BOT_PREFIX}help <command>` "
            + "replacing `<command>` with one "
            + "of the commands listed below. Arguments inside `[]` brackets are optional.\n\u200B"
        )
        embed.set_footer(text="WrapUp help command", icon_url=ICON_URL)

        value = "```digest server\ndigest channel```"
        embed.add_field(name="Digests", inline=True, value=value)

        value = "```\ninvite\nhelp```\n\u200B"
        embed.add_field(name="General", inline=True, value=value)

        learn_more = (
            f"**[Invite Bot]({DISCORD_INVITE})** | "
            + f"**[About WrapUp]({WRAPUP_HOME})** | "
            + f"**[Support]({WRAPUP_DISCORD})**"
        )
        embed.add_field(name="Learn More", inline=False, value=learn_more)
        await ctx.send(embed=embed)

    @help.group(name="digest", invoke_without_command=True)
    async def digest_help(self, ctx):
        embed = discord.Embed(colour=THEME_COLOR)

        embed.title = "Command Help - digest"
        embed.description = (
            "Generate channel and server digests. "
            + f"To find out more about a sub-command, type `{BOT_PREFIX}help digest "
            + "<sub-command>` replacing `<sub-command>` with one."
        )
        embed.set_footer(text="WrapUp help command", icon_url=ICON_URL)

        value = f"```{BOT_PREFIX}<sub-command> [args]```"
        embed.add_field(name="Usage", inline=False, value=value)

        value = "```server, channel```"
        embed.add_field(name="Sub-commands", inline=False, value=value)

        value = f"```{BOT_PREFIX}digest server\n{BOT_PREFIX}digest channel```"
        embed.add_field(name="Examples", inline=False, value=value)

        learn_more = (
            f"**[Invite Bot]({DISCORD_INVITE})** | "
            + f"**[About WrapUp]({WRAPUP_HOME})** | "
            + f"**[Support]({WRAPUP_DISCORD})**"
        )
        embed.add_field(name="Learn More", inline=False, value=learn_more)
        await ctx.send(embed=embed)

    @digest_help.command(name="server")
    async def server_help(self, ctx):
        embed = discord.Embed(colour=THEME_COLOR)

        embed.title = "Command Help - digest server"
        embed.description = "Generate digest for this server for a given period."
        embed.set_footer(text="WrapUp help command", icon_url=ICON_URL)

        value = f"```{BOT_PREFIX}digest server [period]```"
        embed.add_field(name="Usage", inline=False, value=value)

        value = "```[period] - period in days. Must be in range [1 - 10]. Defaults to 1 day.```"
        embed.add_field(name="Arguments", inline=False, value=value)

        value = f"```{BOT_PREFIX}digest server\n{BOT_PREFIX}digest server 7```"
        embed.add_field(name="Examples", inline=False, value=value)

        learn_more = (
            f"**[Invite Bot]({DISCORD_INVITE})** | "
            + f"**[About WrapUp]({WRAPUP_HOME})** | "
            + f"**[Support]({WRAPUP_DISCORD})**"
        )
        embed.add_field(name="Learn More", inline=False, value=learn_more)
        await ctx.send(embed=embed)

    @digest_help.command(name="channel")
    async def channel_help(self, ctx):
        embed = discord.Embed(colour=THEME_COLOR)

        embed.title = "Command Help - digest channel"
        embed.description = "Generate channel digest for a given period."
        embed.set_footer(text="WrapUp help command", icon_url=ICON_URL)

        value = f"```{BOT_PREFIX}digest channel [channel-name] [period]```"
        embed.add_field(name="Usage", inline=False, value=value)

        value = (
            "```[channel-name] - channel for which to generate digest. If not specified, "
            + "generates digest for current channel.\n\n[period] - period in days."
            + " Must be in range [1 - 10]. Defaults to 1 day.```"
        )
        embed.add_field(name="Arguments", inline=False, value=value)

        value = (
            f"```{BOT_PREFIX}digest channel\n{BOT_PREFIX}digest channel #general 7\n"
            + f"{BOT_PREFIX}digest channel #random```"
        )
        embed.add_field(name="Examples", inline=False, value=value)

        learn_more = (
            f"**[Invite Bot]({DISCORD_INVITE})** | "
            + f"**[About WrapUp]({WRAPUP_HOME})** | "
            + f"**[Support]({WRAPUP_DISCORD})**"
        )
        embed.add_field(name="Learn More", inline=False, value=learn_more)
        await ctx.send(embed=embed)
