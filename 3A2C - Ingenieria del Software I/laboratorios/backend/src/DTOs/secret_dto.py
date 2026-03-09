from enum import Enum
from typing import Optional
from pydantic import BaseModel
from models.secret_card_model import Secret



class TypeSecret(str, Enum):
    MURDERER = "Murderer"
    ACCOMPLICE = "Accomplice"
    OTRO = "Otro"


class SecretDTO(BaseModel):
    secret_name: str
    description: Optional[str] = None
    secret_type: TypeSecret
    player_id: Optional[int] = None
    game_id: int
    revealed: bool = False
    image: Optional[str] = None

    def to_model(self):
        return Secret(**self.model_dump())
