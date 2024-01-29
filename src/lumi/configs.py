from dataclasses import dataclass
from dataclass_wizard import JSONWizard
import uuid


def gen_name(obj: any) -> str:
    return f"{obj.__class__.__name__}-{id(obj)}"

class GlobalSerializable(JSONWizard.Meta):
    key_transform_with_dump = "SNAKE"

@dataclass
class Serializable(JSONWizard):
    name: str = ""
    uid: uuid.UUID = uuid.uuid4().int

    def validate(self):
        assert self.name

    def __post_init__(self):
        if not self.name:
            self.name = gen_name(self)
        self.validate()

