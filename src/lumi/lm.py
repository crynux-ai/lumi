from dataclasses import dataclass, field
from typing import Optional

from . import configs
from . import session as s


@dataclass
class LMInferenceOption(configs.Serializable):
    pass


@dataclass
class LM(configs.Serializable):    

    def complete_text(self, query: str, option: LMInferenceOption) -> str:
        raise NotImplementedError()

    def complete_chat(self, query: list[s.Message], option: LMInferenceOption) -> s.Message:
        raise NotImplementedError()
