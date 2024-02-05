import asyncio
from dotenv import dotenv_values,load_dotenv
import os

load_dotenv("./env/discord_bot.env")

import discord
import game_controller
import pixel_enigma
from utils import configs, discord_helper


bot_intent = discord.Intents.default()
bot_intent.members = True
bot_intent.message_content = True
client = discord.Client(intents=bot_intent)
tree = discord.app_commands.CommandTree(client)

game_controller.admin.add_commands(tree)
game_controller.user.add_commands(tree)
pixel_enigma.add_commands(tree)


@client.event
async def on_ready():
    print(f"{client.user} is online for {len(client.guilds)} servers.")
    channels = await discord_helper.get_channels_in_category(
        client.guilds[0], configs.config["discord"]["category_name"])
    assert channels
    print(f"{len(channels)} channels available in the first server")
    print(f"Their member count: {str([len(c.members) for c in channels])}")

    synced = await tree.sync()
    print(f"Ready to play with {len(synced)} commands! Commands: {synced}")


client.run(configs.config["discord"]["token"])
