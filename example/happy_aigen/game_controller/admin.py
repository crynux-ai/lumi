import discord
from game_controller import discord_helper

@discord.app_commands.command(
    name="admin_new_channel", description="Admin add a new private channel for HappyAIGen")
@discord.app_commands.guild_only()
@discord.app_commands.checks.has_permissions(moderate_members=True)
async def admin_new_channel(interaction: discord.Interaction, channel_name: str):
    if not interaction.guild:
        await interaction.response.send_message("Please send message in a discord server instead of DM me")
        return

    channel = await discord_helper.create_private_channel(
        interaction.guild, discord_helper.category_name(), channel_name) 
    await interaction.response.send_message(
        f"Channel [{channel_name}](https://discord.com/channels/{interaction.guild_id}/{channel.id}) is created.")

def add_commands(tree):
    tree.add_command(admin_new_channel)
