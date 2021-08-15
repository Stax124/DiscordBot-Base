import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext.commands.context import Context


async def confirm(bot: Bot, ctx: Context, message: str, timeout: int = 20, author: str = "Confirm") -> bool:
    """Ask a user to confirm an action.

    Args:
        bot (Bot): Just pass your bot instance.
        ctx (Context): Also pass your context.
        message (str): What question you want to ask the user.
        timeout (int, optional): Time to wait for input. Defaults to 20.
        author (str, optional): What should be displayed if Author field inthe embed is not filled. Defaults to "Confirm".

    Returns:
        bool: Accepted or not.
    """

    try:
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(255, 255, 0),
            description=message
        )
        embed.set_author(name=author, icon_url=bot.user.avatar_url)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

        reaction, _ = await bot.wait_for('reaction_add', timeout=timeout, check=check)
        if reaction.emoji == '❌':
            await msg.delete()
            return False
        elif reaction.emoji == '✅':
            await msg.delete()
            return True

    except asyncio.TimeoutError:
        await msg.delete()
        return False
