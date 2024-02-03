import discord
import os


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
	return _get_os_value("PIXEL_ENIGMA_MIN_PLAYER")


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
