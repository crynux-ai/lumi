import asyncio
from dotenv import dotenv_values,load_dotenv
import os

import discord
import user_system


bot_intent = discord.Intents.default()
bot_intent.members = True
bot_intent.message_content = True
client = discord.Client(intents=bot_intent)
tree = discord.app_commands.CommandTree(client)


user_system.add_commands(tree)

@client.event
async def on_ready():
    synced = await tree.sync()
    print(f"Ready to play with {len(synced)} commands! Commands: {synced}")


load_dotenv("./env/discord_bot.env")
client.run(os.getenv("DISCORD_BOT_TOKEN"))
