import argparse
import logging
import os
import sys

import discord
from discord.ext import commands
from discord.ext.commands import AutoShardedBot
from discord.ext.commands.context import Context
from discord.ext.commands.errors import (ExtensionAlreadyLoaded,
                                         ExtensionNotFound, ExtensionNotLoaded)
from pretty_help import PrettyHelp

# Set up parser for command line arguments
parser = argparse.ArgumentParser(
    prog="Trinity", description="Economy discord bot made in python")
parser.add_argument("-l", "--logging",  default="INFO",
                    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Choose level of logging")
parser.add_argument("-f", "--file", type=str, help="Filename for logging")
parser.add_argument("--token", default=os.environ["TRINITY"], type=str,
                    help="Discord API token: Get yours at https://discord.com/developers/applications")
args = parser.parse_args()


# Translate log level from string to its logging counterpart
loglevels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL:": logging.CRITICAL
}

# Set up logging
logging.basicConfig(
    level=loglevels[args.logging], handlers=[logging.FileHandler(args.file, "w", 'utf-8'), logging.StreamHandler(sys.stdout)] if args.file else [logging.StreamHandler(sys.stdout)], format='%(levelname)s | %(asctime)s | %(name)s |->| %(message)s', datefmt=r"%H:%M:%S"
)

# Find all extensions in the cogs folder
default_extensions = ["cogs."+i.replace(".py", "")
                      for i in os.listdir("cogs") if i.endswith(".py")]


def get_prefix(bot, msg):
    """
    A callable Prefix for our bot.

    Allows per server prefixes by setting prefix in the configuration.
    """

    return commands.when_mentioned_or(bot.configs[msg.guild.id]["prefix"])(bot, msg)


class Bot(AutoShardedBot):
    def __init__(self):
        # Initialize the bot with out prefix method and a custom help command
        # Intents are set to all - you need to change setting of your intents at https://discordapp.com/developers/applications/
        super().__init__(
            command_prefix=get_prefix,
            help_command=PrettyHelp(
                color=0xffff00, show_index=True, sort_commands=True),
            intents=discord.Intents.all()
        )

        # Variables to store the bot's configuration and version
        self.configs = {}
        self.__version__ = "1.0"


# Create bot Instance
bot = Bot()

# Command for quick reload of an extension


@bot.command(name="reload")
@commands.is_owner()
async def reload_extension(ctx: Context, extension: str):
    try:
        bot.reload_extension("cogs."+extension)
        logging.info(f"{extension} reloaded")
        embed = discord.Embed(
            color=0xffff00, description=f"{extension} reloaded")
        embed.set_author(name="Reload", icon_url=bot.user.avatar_url)
    except ExtensionNotFound:
        logging.error(f"{extension} not found")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} not found")
        embed.set_author(name="Reload", icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)

# Loads new extension


@bot.command(name="load")
@commands.is_owner()
async def load_extension(ctx: Context, extension: str):
    try:
        bot.load_extension("cogs."+extension)
        logging.info(f"{extension} loaded")
        embed = discord.Embed(
            color=0x00ff00, description=f"{extension} loaded")
        embed.set_author(name="Load", icon_url=bot.user.avatar_url)
    except ExtensionAlreadyLoaded:
        logging.warn(f"{extension} already loaded")
        embed = discord.Embed(
            color=0xffff00, description=f"{extension} already loaded")
        embed.set_author(name="Load", icon_url=bot.user.avatar_url)
    except ExtensionNotFound:
        logging.error(f"{extension} not found")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} not found")
        embed.set_author(name="Load", icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)

# Unloads specified extension


@bot.command(name="unload")
@commands.is_owner()
async def reload_extension(ctx: Context, extension: str):
    try:
        bot.unload_extension("cogs."+extension)
        logging.info(f"{extension} unloaded")
        embed = discord.Embed(
            color=0x00ff00, description=f"{extension} unloaded")
        embed.set_author(name="Unload", icon_url=bot.user.avatar_url)
    except ExtensionNotFound:
        logging.error(f"{extension} not found")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} not found")
        embed.set_author(name="Unload", icon_url=bot.user.avatar_url)
    except ExtensionNotLoaded:
        logging.error(f"{extension} not found")
        embed = discord.Embed(
            color=0xffff00, description=f"{extension} exists, but is not loaded")
        embed.set_author(name="Unload", icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)

# If this is main script, load all extensions and run the bot
if __name__ == "__main__":
    for extension in default_extensions:
        bot.load_extension(extension)
        logging.info(f"{extension} loaded")

    # ! You need to set your enviromental variable TRINITY to your bot token (or just rename the variable betwen the quotes) !
    bot.run(os.environ["TRINITY"], reconnect=True)
