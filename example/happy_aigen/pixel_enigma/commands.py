import discord
from typing import Optional

from game_controller import user
from pixel_enigma import game_system
from utils import storage, configs, discord_helper


game_system = game_system.GameSystem(game_store=storage.InMemoryStore())


class Group(discord.app_commands.Group):

    async def _check_user(self, interaction: discord.Interaction) -> Optional[user.User]:
        u = await user.user_system.query_user(interaction.user.id)
        if not u or not u.current_channel_id:
            await interaction.response.send_message((
                f"Hello, {str(interaction.user)}, can you type `/user join` from "
                f"a [channel]({configs.config["discord"]["public_channel_url"]}) with HappyAIGen bot?"
            ))
            return None
        return u


    @discord.app_commands.command(name="start", description="Start a game")
    @discord.app_commands.guild_only()
    async def start(self, interaction: discord.Interaction):
        u = await self._check_user(interaction)
        if not u:
            return
        if not interaction.guild or interaction.channel_id != u.current_channel_id:
            return await interaction.response.send_message((
                f"Hello, {str(interaction.user)}, can you type `/pixel_enigma start` from your assigned "
                f"[channel]({configs.get_channel_url(u.current_guild_id, u.current_channel_id)})?"
            ))

        await interaction.response.send_message(
            f"Stake {configs.get_credit_str(configs.config["pixel_enigma"]["stake_credit_e8"])}"
            f" credits. Matching players...")
        game, response = await game_system.match(interaction, u)
        if response:
            await interaction.channel.send(response)
        if not game:
            return
        await game_system.start(interaction, u)


    @discord.app_commands.command(
        name="prompt",
        description=(
            "[MUST DM the bot] Enter your prompt to generate the image."))
    async def prompt(self, interaction: discord.Interaction, prompt: str):
        u = await self._check_user(interaction)
        if not u:
            return
        if interaction.guild_id:
            return await interaction.response.send_message("Hey, you probably want to DM me your prompt, right?")
        await game_system.prompt(interaction, u)


def add_commands(tree):
    tree.add_command(Group(
        name="pixel_enigma",
        description="See who's prompt generates closest image"))
