import discord
from utils import discord_helper, configs


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
            interaction.guild, configs.config["discord"]["category_name"], channel_name) 
        await interaction.response.send_message(
            f"Channel [{channel_name}]({configs.get_channel_url(interaction.guild_id)/(channel.id)}) is created.")


    @discord.app_commands.command(
        name="admin_set_maintenance", description="Start maintenance of HappyAIGen")
    @discord.app_commands.choices(status=[
        discord.app_commands.Choice(
            name=configs.SystemMaintenanceStatus.LIVE.name,
            value=configs.SystemMaintenanceStatus.LIVE.value),
        discord.app_commands.Choice(
            name=configs.SystemMaintenanceStatus.IN_MAINTENANCE.name,
            value=configs.SystemMaintenanceStatus.IN_MAINTENANCE.value),
    ])
    async def admin_set_maintenance(self, interaction: discord.Interaction, status: int):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "You need to be an admin of this discord server to run this command")
        configs.set_maintenance(status)
        messages = {
            configs.SystemMaintenanceStatus.LIVE.value:
                "HappyAIGen back to live!",
            configs.SystemMaintenanceStatus.IN_MAINTENANCE.value:
                "Start maintenance, no new jobs can be scheduled",
        }
        return await interaction.response.send_message(messages[status])


def add_commands(tree):
    tree.add_command(Group(
        name="admin",
        description="Admin command panel"))
