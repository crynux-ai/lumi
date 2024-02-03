import asyncio
from dotenv import dotenv_values,load_dotenv
import os

import discord
import game_controller
from game_controller import discord_helper
import pixel_enigma


load_dotenv("./env/discord_bot.env")
bot_intent = discord.Intents.default()
bot_intent.members = True
bot_intent.message_content = True
client = discord.Client(intents=bot_intent)
tree = discord.app_commands.CommandTree(client)


game_controller.add_commands(tree)
pixel_enigma.add_commands(tree)



@client.event
async def on_ready():
    print(f"{client.user} is online for {len(client.guilds)} servers.")
    channels = await discord_helper.get_channels(
        client.guilds[0], discord_helper.category_name())
    assert channels
    print(f"{len(channels)} available in the first server")

    synced = await tree.sync()
    print(f"Ready to play with {len(synced)} commands! Commands: {synced}")


client.run(discord_helper.bot_token())
