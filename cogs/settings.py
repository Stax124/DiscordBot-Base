import json

from core.functions import confirm
from discord.ext import commands
from discord.ext.commands.context import Context


class Settings(commands.Cog):
    "Manage configuration of your server"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="config", help="Dump config for your server")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx: Context):
        """Dump config for your server"""

        await ctx.send(json.dumps(self.bot.configs[ctx.guild.id].config))

    @commands.command(name="version")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx: Context):
        """Dump version of this bot"""

        await ctx.send(self.bot.__version__)

    @commands.command(name="prefix")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: Context, prefix: str):
        """Change prefix for your server

        Args:
            prefix (str): Prefix for your server
        """

        if await confirm(self.bot, ctx, message=f"Change server prefix to `{prefix}` ?"):
            self.bot.configs[ctx.guild.id]["prefix"] = prefix
            self.bot.configs[ctx.guild.id].save()


def setup(bot):
    bot.add_cog(Settings(bot))
