"""Games Schemas."""

from pydantic import BaseModel, Field, constr, model_validator
from DTOs.game_dto import GameDTO
from typing_extensions import Self
from typing import Optional, List
from datetime import date
from models.game_model import Game
from models.player_model import Player
from enum import Enum


class GameFinishReason(str, Enum):
    """Enum for game finish reasons."""

    ALL_DETECTIVES_ELIMINATED = "all detectives on social disgrace"
    MURDERER_ESCAPES = "The murderer escapes"
    MURDERER_REVEALED = "The murderer has been revealed"


class GameIn(BaseModel):
    """
    Schema for representing a inbound Game
    """

    game_name: constr(min_length=1, max_length=50)  # type: ignore
    min_players: int = Field(
        ..., ge=2, le=6
    )  # greater equal than two and less equal than 6
    max_players: int = Field(
        ..., ge=2, le=6
    )  # greater equal than 2 and less equal than 6
    player_name: constr(min_length=1, max_length=50)  # type: ignore
    player_birth_date: date

    def to_dto(self) -> GameDTO:
        return GameDTO(
            name=self.game_name,
            min_players=self.min_players,
            max_players=self.max_players,
            player_name=self.player_name,
            player_birth_date=self.player_birth_date,
        )

    @model_validator(mode="after")
    def check_player_min_max(self) -> Self:
        min_p, max_p = self.min_players, self.max_players
        if min_p > max_p:
            raise ValueError("min_players cannot be greater than max_players")
        return self


class GameResponse(BaseModel):
    """Class for retriving Game creation response."""

    game_id: int
    player_id: int


class PlayerTurnInfo(BaseModel):
    id_jugador: int
    nombre: str
    posicionTurno: int


class TurnResponse(BaseModel):
    id_partida: int
    turnoActual: Optional[PlayerTurnInfo]
    jugadores: list[PlayerTurnInfo]
    enCurso: bool


class StartGameRequest(BaseModel):
    player_id: int


class DrawCardRequest(BaseModel):
    player_id: int
    draftCardsSelectedIds: List[int]
    drawPileSelectedCount: int

class StartGameResponse(BaseModel):
    status: str
    game_id: int


class FinishTurnRequest(BaseModel):
    player_id: int


class SecretEffect(str, Enum):
    HIDE = "HIDE"
    REVEAL = "REVEAL"


class SecretRequest(BaseModel):
    player_id: int
    secret_id: int
    effect: SecretEffect


class SetPlayRequest(BaseModel):
    set_id: int
    target_player_id: int
    chosen_secret_id: Optional[int] = None  
    chosen_set_id: Optional[int] = None 

class SecretSteal(BaseModel):
    player_id: int
    target_player_id: int
    secret_id: int

    