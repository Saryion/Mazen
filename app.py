import discord
import json
import os

from discord.ext import commands

# Reads the config file for personalised configs.
with open("./config.json", "r") as config:
    configData = json.load(config)
    token = configData["token"]
    prefix = configData["prefix"]

client = commands.Bot(command_prefix=prefix)

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

for cogs in os.listdir("./cogs"):
    if cogs.endswith(".py"):
        client.load_extension(f"cogs.{cogs[:-3]}")

client.run(token)
