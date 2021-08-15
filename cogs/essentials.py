from typing import Union

import discord
from core.functions import confirm
from discord.ext import commands
from discord.ext.commands.context import Context


class Essentials(commands.Cog):
    "Esential functions"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge", help="Delete messages from channel")
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx: Context, number_of_messages: int = 100):
        """Cleans X messages from a channel.

        Args:
            number_of_messages (int, optional): Number of messages that will be deleted. Defaults to 100.
        """

        if await confirm(self.bot, ctx, message=f"Clean {number_of_messages} messages ?"):
            await ctx.channel.purge(limit=number_of_messages)

    @commands.command(name="autorole", help="Set default role after member joins")
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx: Context, role: Union[discord.Role, None]):
        """Gives a role to every player that joins the server.

        Args:
            role (Union[discord.Role, None]): Role that will be given to him, leave empty to remove the role.
        """

        if role == None:
            self.bot.configs[ctx.guild.id]["autorole"] = None
        else:
            _id = role.id
            self.bot.configs[ctx.guild.id]["autorole"] = _id

        self.bot.configs[ctx.guild.id].save()

        embed = discord.Embed(
            color=0x00ff00, description=f"Auto-role set to {role.mention if role != None else 'None'}")
        embed.set_author(name="Auto-role", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Essentials(bot))
