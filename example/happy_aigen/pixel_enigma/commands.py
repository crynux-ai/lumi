import dataclasses
import enum
from datetime import datetime
from typing import Union, Optional

import discord
from discord.ext import commands
from utils import storage



class GameStatus(enum.Enum):
    PENDING = 0
    ALL_JOINED = 10
    IMAGE_SELECTED = 20
    PROMPTING = 30
    EVALUATING = 40
    COMPLETED = 50
    FAILED = 60

class GameAction(enum.Enum):
    START = 0
    JOIN = 10
    IMAGE = 20
    PROMPT = 30
    EVALUATE = 40
    COMPLETE = 50
    FAIL = 60


@dataclasses.dataclass
class Game:
    game_id: int
    credit_e8: int
    status: GameStatus

    players_dcuser_id: list[int]
    players_original_credit_e8: list[int]
    players_stake_credit_e8: list[int]
    players_prompts: list[str]
    winner_dcuser_id: int
    actions: list[GameAction]
    action_timestamp_ms: list[int]

    initiator_dcuser_id: int
    initiator_channel_id: int
    initiator_guild_id: int

    worker_cid: list[int]
    worker_credit_e8: list[int]



class GameSystem:

    def __init__(self, game_store: storage.Storage):
        self.game_store = game_store

    async def start(self, interaction: discord.Interaction):
        pass

    async def prompt(self, interaction: discord.Interaction, prompt: str):
        pass


game_system = GameSystem(game_store=storage.InMemoryStorage())


class Group(discord.app_commands.Group):
    @discord.app_commands.command(name="start", description="Start a game")
    async def start(self, interaction: discord.Interaction):
        await interaction.response.send_message("Game start!")


    @discord.app_commands.command(
        name="prompt",
        description=(
            "Enter your prompt to generate the image. Please DM the bot, "
            "so that the prompt is not disclosed to others"))
    async def prompt(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.send_message(f"Your prompt is {prompt}")


def add_commands(tree):
    tree.add_command(Group(
        name="pixel_enigma",
        description="See who's prompt generates closest image"))
