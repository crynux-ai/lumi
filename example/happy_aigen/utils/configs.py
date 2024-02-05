from datetime import datetime
import enum
import os
from pyaml_env import parse_config
from typing import Optional

config = parse_config("setting.yaml")

def current_timestamp_ms() -> int:
    return int(datetime.now().timestamp()*1000)

def get_credit_str(credit_e8: int) -> str:
    return "{:.2f}".format(credit_e8 / 1e8)

def get_channel_url(guild_id: int, channel_id: int) -> str:
    return f"https://discord.com/channels/{guild_id}/{channel_id}"

class SystemMaintenanceStatus(enum.Enum):
    LIVE = 0
    IN_MAINTENANCE = 1

def set_maintenance(status: int):
    os.environ["HAPPY_AIGEN_MAINTENANCE_MODE"] = str(status)

def in_maintenance() -> bool:
    value = os.getenv("HAPPY_AIGEN_MAINTENANCE_MODE")
    return value and int(value) == SystemMaintenanceStatus.IN_MAINTENANCE.value

