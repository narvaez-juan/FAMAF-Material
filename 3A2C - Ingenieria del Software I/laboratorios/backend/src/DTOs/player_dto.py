"""Defines data transfer objects for players (DTOs)"""

from dataclasses import dataclass
from datetime import date


@dataclass
class PlayerDTO:
    name: str
    birthdate: date
