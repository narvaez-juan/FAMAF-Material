from pydantic import BaseModel, constr, model_validator
from DTOs.player_dto import PlayerDTO
from typing_extensions import Self
from datetime import date


class PlayerIn(BaseModel):
    """
    Schema for representing a inbound Player
    """

    player_name: constr(min_length=1, max_length=50)  # type: ignore
    player_dob: date

    def to_dto(self) -> PlayerDTO:
        return PlayerDTO(name=self.player_name, birthdate=self.player_dob)

    @model_validator(mode="after")
    def check_birthdate(self) -> Self:
        if self.player_dob >= date.today():
            raise ValueError("birthdate must be in the past")
        return self
        
class PlayerResponse(BaseModel):
    """Class for retriving Player creation response."""
    player_id: int
    name: str
    birthdate: str
    