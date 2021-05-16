import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx: commands.context, user: discord.Member):
        await self.bot.send()
