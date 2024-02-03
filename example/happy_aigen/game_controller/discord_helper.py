import discord
import os


def _get_os_value(key: str) -> str:
	value = os.getenv(key)
	assert value
	return value


def bot_token() -> str:
	return _get_os_value("HAPPY_AIGEN_CATEGORY_NAME")


def category_name() -> str:
	return _get_os_value("HAPPY_AIGEN_CATEGORY_NAME")


async def get_channels(
	guild: discord.Guild, category_name: str
	) -> list[discord.abc.GuildChannel]:
	for x in guild.categories:
		print(x.name)
	category = discord.utils.get(guild.categories, name=category_name)
	if not category:
		return []
	channels = category.channels
	return channels