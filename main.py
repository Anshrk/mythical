from discord.ext import commands
import os
from dotenv import load_dotenv

# loading .env
load_dotenv()


bot = commands.Bot(command_prefix='myth ')

bot.load_extension('cogs.economy')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def hello(ctx: commands.Context, ):
    await ctx.send("Hello")

bot.run(os.getenv("TOKEN"))
