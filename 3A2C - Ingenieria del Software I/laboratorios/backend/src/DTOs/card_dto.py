from dataclasses import dataclass
from models.game_cards_model import CardLocation

@dataclass
class CardDTO:
    image: str
    type: str
    owner_id: int | None 
    location: CardLocation
