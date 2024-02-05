import asyncio
import dataclasses
import discord
import enum
from typing import Tuple, Optional

from game_controller import user
from utils import storage, configs

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
    channel_id: int
    guild_id: int

    players_dcuser_id: list[int]
    players_original_credit_e8: list[int]
    players_stake_credit_e8: list[int]
    players_prompts: list[str]
    winner_dcuser_id: int

    actions: list[GameAction]
    action_timestamp_ms: list[int]
    action_details: list[str]

    worker_cid: list[int]
    worker_credit_e8: list[int]



class GameSystem:

    def __init__(self, game_store: storage.Storage):
        self.game_store = game_store
        self.pending_game = {}
        self.pending_barrier = {}

    async def start(self, interaction: discord.Interaction, u: user.User) -> Tuple[Optional[Game], str]:
        if u.credit_e8 < configs.config["pixel_enigma"]["stake_credit_e8"]:
            return None, (
                f"Hello, {interaction.user.mention}, you don't have enough credit to start a game. "
                f"Try to invite more friends or run a Crynux node to earn credits.")
        if u.current_channel_id not in self.pending_game:
            self.pending_game[u.current_channel_id] = Game(
                # TODO: setup game id
                game_id=0,
                credit_e8=0,
                status=GameStatus.PENDING,
                channel_id=u.current_channel_id,
                guild_id=u.current_guild_id,
                players_dcuser_id=[],
                players_original_credit_e8=[],
                players_stake_credit_e8=[],
                players_prompts=[],
                winner_dcuser_id=0,
                actions=[GameAction.START],
                action_timestamp_ms=[configs.current_timestamp_ms()],
                action_details=[""],
                worker_cid=[],
                worker_credit_e8=[],
            )
            self.pending_barrier[u.current_channel_id] = asyncio.Barrier(
                configs.config["pixel_enigma"]["min_player"])

        game = self.pending_game[u.current_channel_id]
        if u.discord_userid in game.players_dcuser_id:
            return None, (
                f"Hello, {interaction.user.mention}, you are already in waiting queue,"
                f" just wait {configs.config["pixel_enigma"]["match_timeout_sec"]} seconds")
        game.players_dcuser_id.append(u.discord_userid)
        game.players_original_credit_e8.append(u.credit_e8)
        # TODO: add a lock on user credit right after check.
        u.credit_e8 -= configs.config["pixel_enigma"]["stake_credit_e8"]
        game.players_stake_credit_e8.append(
            configs.config["pixel_enigma"]["stake_credit_e8"])
        try:
            async with asyncio.timeout(configs.config["pixel_enigma"]["match_timeout_sec"]):
                await self.pending_barrier[u.current_channel_id].wait()
            game.status = GameStatus.ALL_JOINED
            self.game_store.insert(game.game_id, game)
            
            if u.current_channel_id in self.pending_game:
                self.pending_game.pop(u.current_channel_id)
                self.pending_barrier.pop(u.current_channel_id)
                return game, "Hello, Game Start!"
            else:
                return game, ""
        except TimeoutError:
            game.status = GameStatus.FAILED
            game.actions.append(GameAction.FAIL)
            game.action_timestamp_ms.append(configs.current_timestamp_ms())
            u.credit_e8 += configs.config["pixel_enigma"]["stake_credit_e8"]
            game.action_details.append(
                f"Timeout with {self.pending_barrier[interaction.channel_id].n_waiting} players")
            return None, f"Sorry, {interaction.user.mention}, we haven't matched any players with you, try again later."


    async def prompt(self, interaction: discord.Interaction, prompt: str):
        pass
