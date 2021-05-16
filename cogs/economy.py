from discord.ext import commands
import discord
import random
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# setting up the environment variables
load_dotenv()


# setting up the database
cluster = MongoClient(os.getenv("DB_URI"))
leveling = cluster['discord']['leveling']


def RandomColorGenerator() -> str:
    """ Generate Random hex values """
    hex_nu = random.randint(0, 16777215)
    return format(hex_nu, 'x')


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        stats = leveling.find_one({"id": message.author.id})
        if not message.author.bot:
            if stats is None:
                newUser = {"id": message.author.id, "xp": 100}
                leveling.insert_one(newUser)
            else:
                xp = stats["xp"] + 5
                leveling.update({"id": message.author.id},
                                {'$set': {'xp': xp}})
                lvl = 0
                while True:
                    if xp < ((50*(lvl**2))+(50*lvl-1)):
                        break
                    lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                if xp == 0:
                    myEmbed = {
                        "title": "Nice Job",
                        "description":
                        f"{message.author.mention} just leveled up",
                        "color": int("0x"+RandomColorGenerator()),
                        "fields": [
                            {"name": "level", "value": "{}".format(lvl)}
                        ],
                        "thumbnail": {"url": message.author.avatar_url}
                    }
                    await message.channel.send(
                        embed=discord.Embed.from_dict(myEmbed)
                    )

    @commands.command()
    async def rank(self, ctx, user: discord.member = None):
        stats = leveling.find_one({"id": ctx.author.id})
        if stats is None:
            embed = discord.Embed(
                description="You haven't sent any messages yet, No Rank!!!")
            await ctx.channel.send(embed=embed)
        else:
            xp = stats["xp"]
            lvl = 0
            rank = 0
            while True:
                if xp < ((50*(lvl**2))+(50*lvl)):
                    break
                lvl += 1
            xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
            boxes = int((xp/(200*((1/2) * lvl)))*20)
            ranking = leveling.find().sort("xp", -1)
            for x in ranking:
                rank += 1
                if stats["id"] == x["id"]:
                    break

            embed = discord.Embed(title=f"{ctx.author.name}'s level stats")
            embed.add_field(name="Name", value=ctx.author.mention, inline=True)
            embed.add_field(
                name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True
            )
            embed.add_field(
                name="Rank", value=f"{rank}/{ctx.guild.member_count}",
                inline=True
            )
            embed.add_field(
                name="Progress Bar [lvl]", value=boxes * ":blue_square:" +
                (20-boxes) * ":white_large_square:", inline=False
            )
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):
        ranking = leveling.find().sort("xp", -1)
        i = 1
        embed = discord.Embed(title="Rankings:")
        for x in ranking:
            try:
                temp = ctx.guild.get_member(x["id"])
                tempxp = x["xp"]
                embed.add_field(name=f"{i}: {temp.name}",
                                value=f"Total XP: {tempxp}", inline=False)
                i += 1
            except Exception:
                pass
            if i == 11:
                break
        await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(Economy(client))
