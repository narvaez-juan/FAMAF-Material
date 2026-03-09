"""Card Schemas"""

from typing import List, Optional
from pydantic import BaseModel
from DTOs.card_dto import CardDTO
from models.game_cards_model import CardLocation

class CardIn(BaseModel):
    image: str
    type: str
    owner_id: int
    location: CardLocation

    def to_dto(self) -> CardDTO:
        return CardDTO(
            image= self.image,
            type= self.type,
            owner_id= self.owner_id,
            location= self.location
        )  

class CardInfo(BaseModel):
    id: int
    image: str
    type: str
    owner_id: int
    location: CardLocation

class CardResponse(BaseModel):
    cards: List[CardInfo]

class CardRequest(BaseModel):
    card_ids: list[int] 

class DiscardActionResponse(BaseModel):
    game_id: int
    player_id: int
    discarded_cards: list[int]
    updated_hand: list[int]

class CardsOffTableRequest(BaseModel):
  player_id: int               
  id_card: int                 
  target_player_id: int 

class AnotherVictimRequest(BaseModel):
    set_id: int
    event_card_id: int

class DeadCardFollyRequest(BaseModel):
    direction: str
    cards_to_pass: list[list[int]]
    id_dead_card_folly: int

class DelayTheMurdererEscapeRequest(BaseModel):
    id_delay_the_murderer_escape: int
    player_id:int
    cards_selected:list[int]

class EarlyTrainToPaddingtonRequest(BaseModel):
    id_early_train_to_paddington: int
    player_id: int




class LookIntoRequest(BaseModel):
    event_card_id: int
    chosen_gamecard_id: int 
    
class PointYourSuspicionRequest(BaseModel):
    player_id: int
    card_id: int
    target_player_ids: list[int]