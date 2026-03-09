# Import all models to ensure they're registered
from .card_model import Card
from .game_model import Game
from .game_cards_model import GameCards
from .player_model import Player  # If you have a player model
from .secret_card_model import Secret
from .set_model import SetPlay
__all__ = ['Card', 'Game', 'GameCards', 'Player', 'Secret', 'SetPlay']