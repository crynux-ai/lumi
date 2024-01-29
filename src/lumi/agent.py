from dataclasses import dataclass, field
from typing import Optional

from . import configs
from . import session as s


@dataclass
class LMInferenceOption(configs.Serializable):
    pass


@dataclass
class LM(configs.Serializable):    

    def generate(self, query: str, option: LMInferenceOption) -> str:
        raise NotImplementedError()
