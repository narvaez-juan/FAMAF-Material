"""Schemas para la entidad Secreto."""
from pydantic import BaseModel
from enum import Enum
from typing import Optional
from models.secret_card_model import Secret

class TypeSecret(str, Enum):
    MURDERER = "Murderer"
    ACCOMPLICE = "Accomplice"
    OTRO = "Otro"


class SecretBase(BaseModel):
    secret_name: str
    description: Optional[str] = None
    secret_type: TypeSecret
    player_id: int
    game_id: int
    revealed: bool = False
    
    def to_model(self) -> Secret:
        return Secret(
            secret_name=self.secret_name,
            description=self.description,
            secret_type=self.type_secret,
            player_id=self.player_id,
            game_id=self.game_id,
            revealed=self.revealed
        )
