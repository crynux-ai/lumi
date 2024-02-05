import discord
from typing import Optional


async def get_channels_in_category(
    guild: discord.Guild, category_name: str) -> list[discord.abc.GuildChannel]:
    if not guild:
        return []
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        return []
    return category.channels


async def add_user_to_channel(channel: discord.abc.GuildChannel, member: discord.Member):
    perms = channel.overwrites_for(member)
    perms.send_messages = True
    perms.read_messages = True
    # perms.view_channel = True 
    await channel.set_permissions(member, overwrite=perms, reason="Join")


async def create_private_channel(
    guild: discord.Guild, category_name: str, channel_name: str) -> Optional[discord.TextChannel]:

    parent = guild
    if category_name:
        parent = discord.utils.get(guild.categories, name=category_name)
        if not parent:
            return None

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        guild.me: discord.PermissionOverwrite(view_channel=True)
    }
    return await parent.create_text_channel(channel_name, overwrites=overwrites)
