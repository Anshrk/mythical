from discord.ext import commands
import discord


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass
