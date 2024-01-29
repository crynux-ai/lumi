import asyncio
from dotenv import dotenv_values,load_dotenv
import os

import discord

load_dotenv("./env/discord_bot.env")

bot_intent = discord.Intents.default()
bot_intent.members = True
bot_intent.message_content = True
client = discord.Client(intents=bot_intent)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

client.run(os.getenv("DISCORD_BOT_TOKEN"))
