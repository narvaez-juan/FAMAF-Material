"""Defines data transfer objects for games (DTOs)"""

from dataclasses import dataclass
from datetime import date

@dataclass
class GameDTO:
    name: str
    min_players: int
    max_players: int
    player_name: str 
    player_birth_date: date




