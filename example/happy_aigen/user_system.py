from typing import Union

import discord
from discord.ext import commands


class UserSystem:

    def new_user(self, user: Union[discord.User, discord.Member]):
        user.id

    def show_credit(self, user):
        pass

    def change_credit(self, user, credit_delta):
        pass


user_system = UserSystem()

@discord.app_commands.command(
    name="join", description="Join the game system with a simple click")
async def join(interaction: discord.Interaction):
    existed_user = user_system.new_user(interaction.user)
    if existed_user:
        await interaction.response_send_message((
            f"Hello, {str(interaction.user)}, you've already joined Happy AIGen. "
            f"You have {existed_user.credit} credits. Have fun!"
        ))
    else:
        await interaction.response.send_message((
            f"Hello, {str(interaction.user)}, welcome to Happy AIGen. "
            f"You are rewarded with {100} credits. Have fun!"
        ))


@discord.app_commands.command(
    name="credit_show", description="show your current credit")
async def credit_show(interaction: discord.Interaction):
    await interaction.response.send_message((
        f"Hello, {str(interaction.user)}, your current credit: "
        f"{user_system.show_credit(interaction.author)}"
    ))


def add_commands(tree):
    tree.add_command(join)
    tree.add_command(credit_show)
