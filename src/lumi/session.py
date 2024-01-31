from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from . import configs


@dataclass
class Message(configs.Serializable):
    author: str = ""
    content: str = ""
    timestamp_ms: int = 0

    def validate(self):
        assert self.timestamp_ms > 0
        assert self.author
        assert self.content

    def __post_init__(self):
        if not self.timestamp_ms:
            self.timestamp_ms = int(datetime.now().timestamp()*1000)
        self.validate()

@dataclass
class MessageChannel(configs.Serializable):
    messages: list[Message] = field(default_factory=list)
    
    def add_message(self, user: str, content: str):
        self.messages.append(Message(user, content))

    def get_last_message(self) -> Optional[Message]:
        if messages:
            return messages[-1]
        else:
            return None


@dataclass
class Session(configs.Serializable):
    message_channel: list[MessageChannel] = field(default_factory=list)

    def add_message(self, user: str, content: str):
        for c in self.message_channel:
            c.add_message(user, content)


