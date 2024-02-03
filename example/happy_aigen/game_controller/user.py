import asyncio
import dataclasses
from datetime import datetime
import os
from typing import Union, Optional

import discord
from utils import storage
from game_controller import discord_helper

@dataclasses.dataclass
class User:
    # Import fields in HappyAIGen
    discord_userid: int 
    credit_e8: int
    last_active_timestamp_ms: int

    # Contents from Discord
    global_name: str
    name: str
    source_channel_id: int
    source_guild_id: int
    current_channel_id: int

    def get_credit_str(self) -> str:
        return "{:.2f}".format(self.credit_e8 / 1e8)


class UserSystem:

    def __init__(self, user_store: storage.Storage):
        self.user_store = user_store

    async def query_user(self, dcuser_id: int) -> Optional[User]:
        user =  await self.user_store.query(dcuser_id)
        if user:
            return User(**user)
        else:
            return None

    async def update_user(self, user: User):
        await self.user_store.update(user.discord_userid, dataclasses.asdict(user))

    async def new_user(self, interaction: discord.Interaction) -> Optional[User]:
        user = await self.query_user(interaction.user.id)
        if user:
            return user
        user = User(
            discord_userid=interaction.user.id,
            credit_e8=100 * 100_000_000,
            last_active_timestamp_ms=int(datetime.now().timestamp() * 1000),
            global_name=interaction.user.global_name or "",
            name=interaction.user.name or "",
            source_channel_id=interaction.channel_id or 0,
            source_guild_id=interaction.guild_id or 0,
            current_channel_id=0,
        )
        await self.user_store.insert(interaction.user.id, dataclasses.asdict(user))
        return user

    async def show_credit(self, interaction: discord.Interaction) -> Optional[str]:
        user = await self.query_user(interaction.user.id)
        if user:
            return user.get_credit_str()
        else:
            return None

    async def change_credit(self, dcuser, credit_delta) -> Optional[User]:
        raise NotImplementedError()



user_system = UserSystem(user_store=storage.InMemoryStore())

@discord.app_commands.command(
    name="join", description="Join HappyAIGen with a simple click")
async def join(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message((
            f"Hello, {str(interaction.user)}, can you type `/join` from "
            f"a [channel]({discord_helper.public_channel_url()}) with HappyAIGen bot?"
        ))
        return

    # Add user to the system
    existed_user = await user_system.new_user(interaction)
    if existed_user and existed_user.current_channel_id:
        await interaction.response.send_message((
            f"Hello, {str(interaction.user)}, you've already joined HappyAIGen. "
            f"You have {existed_user.get_credit_str()} credits. Have fun!"
        ))
        return

    # Find channel with least member to join
    channels = await discord_helper.get_channels(
        interaction.guild, discord_helper.category_name())
    min_member = 100_000_000_000
    join_channel = None
    for c in channels:
        if len(c.members) < min_member:
            min_member = len(c.members)
            join_channel = c
    if not join_channel:
        await interaction.response.send_message((
            f"Hello, {str(interaction.user)}, {interaction.guild.name} contains {len(channels)} "
            f"channels. We could not join it. Yell at the admin to fix it."
        ))
        return

    if interaction.guild.me not in join_channel.members:
        await interaction.response.send_message((
            f"Hello, {str(interaction.user)}, HappyAIGen is not in {interaction.guild.name}:{join_channel.name}. "
            f"Yell at the admin to fix it."
        ))
        return

    await discord_helper.add_user_to_channel(join_channel, interaction.user)
    existed_user.current_channel_id = join_channel.id
    await asyncio.gather(
        user_system.update_user(existed_user),
        interaction.response.send_message((
            f"Hello, {str(interaction.user)}, welcome to HappyAIGen. "
            f"You are rewarded with {100} credits. Have fun!"
        )),
        join_channel.send(
            f"Welcome {interaction.user.mention} to {join_channel.name}")
    )



@discord.app_commands.command(
    name="credit_show", description="Show your current credit in HappyAIGen")
async def credit_show(interaction: discord.Interaction):
    credit = await user_system.show_credit(interaction)
    if credit is not None:
        await interaction.response.send_message(
            f"Hello, {str(interaction.user)}, your current credit: {credit}")
    else:
        await interaction.response.send_message((
            f"Hello, {str(interaction.user)}, you haven't joined HappyAIGen yet."
            f"Please use command /join to join."
        ))

def add_commands(tree):
    tree.add_command(join)
    tree.add_command(credit_show)
