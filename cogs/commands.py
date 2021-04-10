import aiohttp
import datetime
import discord
import json

from discord.ext import commands
from quickchart import QuickChart

qc = QuickChart()
qc.width = 1400
qc.height = 800
qc.device_pixel_ratio = 2.0

aq3d_api = "https://game.aq3d.com/api/game/ServerList"


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.client.user}!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Response: {round(self.client.latency * 1000)}ms")

    @commands.command()
    async def aqserver(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=aq3d_api) as response:
                data = await response.json()

        with open("./qc_config.json", "r") as config:
            qc_config = json.load(config)
            qc_config["data"]["datasets"][0]["data"] = [data[0]["UserCount"]]
            qc_config["data"]["datasets"][1]["data"] = [data[2]["UserCount"]]
            qc_config["data"]["datasets"][2]["data"] = [data[4]["UserCount"]]
            qc_config["data"]["datasets"][3]["data"] = [data[5]["UserCount"]]

        qc.config = qc_config

        embed = discord.Embed(title="", description="", colour=discord.Colour(0x800000))
        embed.set_author(name="AQ3D - Server Status", icon_url="https://i.imgur.com/rqpX3dJ.png")
        embed.set_image(url=qc.get_short_url())
        embed.set_footer(text="Saryion#0001 - Github.com/Saryion/Mazen", icon_url="https://i.imgur.com/FeJUMrT.png")

        embed.add_field(name="Red Dragon", value=f":red_circle: {data[0]['UserCount']} / {data[0]['MaxUsers']}", inline=True)
        embed.add_field(name="Blue Dragon", value=f":blue_circle: {data[2]['UserCount']} / {data[2]['MaxUsers']}", inline=True)
        embed.add_field(name="Green Dragon (EU)", value=f":green_circle: {data[4]['UserCount']} / {data[4]['MaxUsers']}", inline=True)
        embed.add_field(name="Gold Dragon (SEA)", value=f":yellow_circle: {data[5]['UserCount']} / {data[5]['MaxUsers']}", inline=True)
        embed.add_field(name="Players", value=f" {data[0]['UserCount'] + data[2]['UserCount'] + data[4]['UserCount'] + data[5]['UserCount']} / {data[0]['MaxUsers'] + data[2]['MaxUsers'] + data[4]['MaxUsers'] + data[5]['MaxUsers']}", inline=True)
        embed.add_field(name="Last Updated", value=f" {data[0]['LastUpdated']}", inline=True)

        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
