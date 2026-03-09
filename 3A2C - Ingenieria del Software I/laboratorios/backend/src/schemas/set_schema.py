from typing import List
from pydantic import BaseModel

class SetIn(BaseModel):
    """
    Schema for representing an inbound Set
    """

    card_ids: List[int]

class StealSet(BaseModel):
    """
    Schema for representing a Steal Set action
    """

    set_id: int

class AriadneJoinRequest(BaseModel):
    ariadne_card_id: int
    target_set_id: int
    player_id: int 


class DetectiveJoinRequest(BaseModel):
    detective_card_id: int 
    target_set_id: int
    player_id: int 