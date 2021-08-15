import logging

import discord
from core.config import Configuration
from discord.activity import Activity
from discord.enums import ActivityType
from discord.ext import commands


class Listeners(commands.Cog):
    "Listeners for bot, feel free to add your own"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        logging.info("Bot sucessfully connected to Discord servers")

    @commands.Cog.listener()
    async def on_connected(self):
        logging.info("Connected to Discord servers")

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"Guilds joined: {len(self.bot.guilds)}")

        for guild in self.bot.guilds:
            config = Configuration(guild.id)
            config.load()
            self.bot.configs[guild.id] = config

        await self.bot.change_presence(activity=Activity(name=f"{len(self.bot.guilds)} servers", type=ActivityType.watching))

    @commands.Cog.listener()
    async def on_disconnect(self):
        logging.info("Bot lost connection to Discord servers")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.bot.change_presence(activity=Activity(name=f"{len(self.bot.guilds)} servers", type=ActivityType.watching))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await self.bot.change_presence(activity=Activity(name=f"{len(self.bot.guilds)} servers", type=ActivityType.watching))


def setup(bot):
    bot.add_cog(Listeners(bot))
