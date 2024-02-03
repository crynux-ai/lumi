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


class UserSystem:

    def __init__(self, user_store: storage.Storage):
        self.user_store = user_store

    async def new_user(self, interaction: discord.Interaction) -> Optional[User]:
        vuser = await self.user_store.query(interaction.user.id)
        if vuser:
            return vuser
        vuser = User(
            discord_userid=interaction.user.id,
            credit_e8=100 * 100_000_000,
            last_active_timestamp_ms=int(datetime.now().timestamp() * 1000),
            global_name=interaction.user.global_name or "",
            name=interaction.user.name or "",
            source_channel_id=interaction.channel_id or 0,
            source_guild_id=interaction.guild_id or 0,
        )
        await self.user_store.insert(interaction.user.id, dataclasses.asdict(vuser))
        return None

    async def show_credit(self, interaction: discord.Interaction) -> Optional[str]:
        vuser = await self.user_store.query(interaction.user.id)
        if vuser:
            return "{:.2f}".format(vuser["credit_e8"] / 1e8)
        else:
            return None

    async def change_credit(self, dcuser, credit_delta) -> Optional[User]:
        raise NotImplementedError()



user_system = UserSystem(user_store=storage.InMemoryStore())

@discord.app_commands.command(
    name="join", description="Join HappyAIGen with a simple click")
async def join(interaction: discord.Interaction):
    existed_user = await user_system.new_user(interaction)

    if existed_user:
        await interaction.response.send_message((
            f"Hello, {str(interaction.user)}, you've already joined HappyAIGen. "
            f"You have {existed_user.credit} credits. Have fun!"
        ))
    else:
        await interaction.response.send_message((
            f"Hello, {str(interaction.user)}, welcome to HappyAIGen. "
            f"You are rewarded with {100} credits. Have fun!"
        ))


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
