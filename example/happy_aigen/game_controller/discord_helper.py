import discord
import enum
import os
from typing import Optional


### OS Env settings ###
def _get_os_value(key: str) -> str:
    value = os.getenv(key)
    assert value
    return value


def bot_token() -> str:
    return _get_os_value("HAPPY_AIGEN_DISCORD_BOT_TOKEN")

def category_name() -> str:
    return _get_os_value("HAPPY_AIGEN_CATEGORY_NAME")

def public_channel_url() -> str:
    return _get_os_value("HAPPY_AIGEN_PUBLIC_CHANNEL_URL")

def pixel_enigma_min_player() -> int:
    return int(_get_os_value("PIXEL_ENIGMA_MIN_PLAYER"))


class SystemMaintenanceStatus(enum.Enum):
    LIVE = 0
    IN_MAINTENANCE = 1


def set_maintenance(status: int):
    os.environ["HAPPY_AIGEN_MAINTENANCE_MODE"] = str(status)


def in_maintenance() -> bool:
    value = os.getenv("HAPPY_AIGEN_MAINTENANCE_MODE")
    return value and int(value) == SystemMaintenanceStatus.IN_MAINTENANCE.value



#### Discord Channels ####
async def get_channels(
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
