import discord
from game_controller import user
from pixel_enigma import game_system
from utils import storage, configs


game_system = game_system.GameSystem(game_store=storage.InMemoryStore())


class Group(discord.app_commands.Group):
    @discord.app_commands.command(name="start", description="Start a game")
    @discord.app_commands.guild_only()
    async def start(self, interaction: discord.Interaction):
        u = await user.user_system.query_user(interaction.user.id)
        if not u or not u.current_channel_id:
            return await interaction.response.send_message((
                f"Hello, {str(interaction.user)}, can you type `/user join` from "
                f"a [channel]({configs.config["discord"]["public_channel_url"]}) with HappyAIGen bot?"
            ))
        if not interaction.guild or interaction.channel_id != u.current_channel_id:
            return await interaction.response.send_message((
                f"Hello, {str(interaction.user)}, can you type `/pixel_enigma start` from your assigned "
                f"[channel]({configs.get_channel_url(u.current_guild_id, u.current_channel_id)})?"
            ))

        await interaction.response.send_message(
            f"Stake {configs.get_credit_str(configs.config["pixel_enigma"]["stake_credit_e8"])}"
            f" credits. Matching players...")
        game, response = await game_system.start(interaction, u)
        if response:
            await interaction.channel.send(response)


    @discord.app_commands.command(
        name="prompt",
        description=(
            "[MUST DM the bot] Enter your prompt to generate the image."))
    async def prompt(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.send_message(f"Your prompt is {prompt}")


def add_commands(tree):
    tree.add_command(Group(
        name="pixel_enigma",
        description="See who's prompt generates closest image"))
