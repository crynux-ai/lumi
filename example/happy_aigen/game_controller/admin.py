import discord
from game_controller import discord_helper


class Group(discord.app_commands.Group):

    @discord.app_commands.command(
        name="admin_new_channel", description="Admin add a new private channel for HappyAIGen")
    @discord.app_commands.guild_only()
    async def admin_new_channel(self, interaction: discord.Interaction, channel_name: str):
        if not interaction.guild:
            return await interaction.response.send_message(
                "Please send message in a discord server instead of DM me")
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "You need to be an admin of this discord server to run this command")

        channel = await discord_helper.create_private_channel(
            interaction.guild, discord_helper.category_name(), channel_name) 
        await interaction.response.send_message(
            f"Channel [{channel_name}](https://discord.com/channels/{interaction.guild_id}/{channel.id}) is created.")


    @discord.app_commands.command(
        name="admin_set_maintenance", description="Start maintenance of HappyAIGen")
    @discord.app_commands.choices(status=[
        discord.app_commands.Choice(
            name=discord_helper.SystemMaintenanceStatus.LIVE.name,
            value=discord_helper.SystemMaintenanceStatus.LIVE.value),
        discord.app_commands.Choice(
            name=discord_helper.SystemMaintenanceStatus.IN_MAINTENANCE.name,
            value=discord_helper.SystemMaintenanceStatus.IN_MAINTENANCE.value),
    ])
    async def admin_set_maintenance(self, interaction: discord.Interaction, status: int):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "You need to be an admin of this discord server to run this command")
        discord_helper.set_maintenance(status)
        messages = {
            discord_helper.SystemMaintenanceStatus.LIVE.value:
                "HappyAIGen back to live!",
            discord_helper.SystemMaintenanceStatus.IN_MAINTENANCE.value:
                "Start maintenance, no new jobs can be scheduled",
        }
        return await interaction.response.send_message(messages[status])


def add_commands(tree):
    tree.add_command(Group(
        name="admin",
        description="Admin command panel"))
