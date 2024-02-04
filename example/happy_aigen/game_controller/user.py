import asyncio
import dataclasses
from datetime import datetime
import os
from typing import Union, Optional

import discord
from utils import storage
from game_controller import admin
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
    current_guild_id: int

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
            current_guild_id=0,
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

class Group(discord.app_commands.Group):

    @discord.app_commands.command(
        name="join", description="Join HappyAIGen with a simple click")
    @discord.app_commands.guild_only()
    async def join(self, interaction: discord.Interaction):
        if not interaction.guild:
            return await interaction.response.send_message((
                f"Hello, {str(interaction.user)}, can you type `/user join` from "
                f"a [channel]({discord_helper.public_channel_url()}) with HappyAIGen bot?"
            ))

        if discord_helper.in_maintenance():
            return await interaction.response.send_message((
                f"HappyAIGen is in maintenance, yell at the admin to resolve it."
            ))

        # Add user to the system
        existed_user = await user_system.new_user(interaction)
        if existed_user and existed_user.current_channel_id:
            check_user_in_channel = False
            channel = discord.utils.get(interaction.guild.channels, id=existed_user.current_channel_id)
            if channel and interaction.user in channel.members:
                check_user_in_channel = True

            if check_user_in_channel:
                channel_url = discord_helper.get_channel_url(
                    existed_user.current_guild_id, existed_user.current_channel_id)
                return await interaction.response.send_message((
                    f"Hello, {str(interaction.user)}, you've already joined "
                    f"HappyAIGen in this [channel]({channel_url})."
                    f"You have {existed_user.get_credit_str()} credits. Have fun!"
                ))

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
            return await interaction.response.send_message((
                f"Hello, {str(interaction.user)}, {interaction.guild.name} contains {len(channels)} "
                f"channels. We could not join any channel. Yell at the admin to fix it."
            ))

        if interaction.guild.me not in join_channel.members:
            return await interaction.response.send_message((
                f"Hello, {str(interaction.user)}, HappyAIGen is not in {interaction.guild.name}:{join_channel.name}. "
                f"Yell at the admin to fix it."
            ))

        channel_url = discord_helper.get_channel_url(interaction.guild.id, join_channel.id)
        channel_message = f"[Channel {join_channel.name}]({channel_url})"

        if existed_user.current_channel_id == 0:
            response_message = (
                f"Hello, {str(interaction.user)}, welcome to HappyAIGen. "
                f"You are rewarded with {existed_user.get_credit_str()} credits. Have fun in {channel_message}!"
            )
        else:
            response_message = (
                f"Hello, {str(interaction.user)}, we've added you back. "
                f"You have {existed_user.get_credit_str()} credits. Have fun in {channel_message}!"
            )


        await discord_helper.add_user_to_channel(join_channel, interaction.user)
        existed_user.current_channel_id = join_channel.id
        existed_user.current_guild_id = interaction.guild_id
        await asyncio.gather(
            user_system.update_user(existed_user),
            interaction.response.send_message(response_message),
            join_channel.send(
                f"Welcome {interaction.user.mention} to {join_channel.name}")
        )


    @discord.app_commands.command(
        name="credit_show", description="Show your current credit in HappyAIGen")
    async def credit_show(self, interaction: discord.Interaction):
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
     tree.add_command(Group(
        name="user",
        description="User command panel"))
