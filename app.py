import discord
import json
import os

from discord.ext import commands

with open("./config.json", "r") as file:
    config = json.load(file)
    token = config["token"]


def fetch_prefix(client, message):
    with open("./prefixes.json", "r") as file:
        prefixes = json.load(file)
    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=fetch_prefix)


async def on_guild_join(guild):
    with open("./prefixes.json", "r") as file:
        prefixes = json.load(file)
    prefixes[str(guild.id)] = "!"

    with open("./prefixes.json", "w") as file:
        json.dump(prefixes, file, indent=2)


@client.event
async def on_guild_remove(guild):
    with open("./prefixes.json", "r") as file:
        prefixes = json.load(file)
    prefixes.pop(str(guild.id))

    with open("./prefixes.json", "w") as file:
        json.dump(prefixes, file, indent=2)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("This command does not exist in my commands.")


@client.command()
async def load(extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(extension):
    client.unload_extension(f"cogs.{extension}")


@client.command()
async def reload(extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

for cogs in os.listdir("./cogs"):
    if cogs.endswith(".py"):
        client.load_extension(f"cogs.{cogs[:-3]}")

client.run(token)
