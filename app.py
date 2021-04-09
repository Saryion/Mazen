import aiohttp
import asyncio
import datetime
import discord
import json

from quickchart import QuickChart

# Some initiate setup for QuickChart.
qc = QuickChart()
qc.width = 1400
qc.height = 800
qc.device_pixel_ratio = 2.0

# The AQ3D API for retrieving player counts.
aq3d_api = "https://game.aq3d.com/api/game/ServerList"

# Reads the config file for personalised configs.
with open("./config.json", "r") as config:
    configData = json.load(config)
    token = configData["token"]
    prefix = configData["prefix"]

class Mazen(discord.Client):
    async def on_ready(self):
        print(f"Launched as {self.user}!")

    async def on_message(self, message):
        if message.author == client.user:
            return

        # The command for requesting the player counts.
        if message.content.startswith(f"{prefix}aqserver"):
            async with aiohttp.ClientSession() as session:
                async with session.get(url=aq3d_api) as response:
                    data = await response.json()

            # Pulling the config data for the bar graph from the qc config file.
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
            embed.set_footer(text="Created by Saryion#0001 - Github.com/Saryion/Mazen")
            embed.timestamp = datetime.datetime.utcnow()

            embed.add_field(name="Red Dragon", value=f":red_circle: {data[0]['UserCount']} / {data[0]['MaxUsers']}", inline=True)
            embed.add_field(name="Blue Dragon", value=f":blue_circle: {data[2]['UserCount']} / {data[2]['MaxUsers']}", inline=True)
            embed.add_field(name="Green Dragon (EU)", value=f":green_circle: {data[4]['UserCount']} / {data[4]['MaxUsers']}", inline=True)
            embed.add_field(name="Gold Dragon (SEA)", value=f":yellow_circle: {data[5]['UserCount']} / {data[5]['MaxUsers']}", inline=True)
            embed.add_field(name="Players", value=f" {data[0]['UserCount'] + data[2]['UserCount'] + data[4]['UserCount'] + data[5]['UserCount']} / {data[0]['MaxUsers'] + data[2]['MaxUsers'] + data[4]['MaxUsers'] + data[5]['MaxUsers']}", inline=True)
            embed.add_field(name="Last Updated", value=f" {data[0]['LastUpdated']}", inline=True)

            await message.channel.send(embed=embed)

client = Mazen()
client.run(token)
