import pytest
from datetime import datetime
from models.game_cards_model import CardLocation, GameCards
from models.game_model import Game
from models.player_model import Player
from models.card_model import Card
from repositories.game_cards_repository import GameCardsRepository
from conftest import create_test_card, create_card_in_db, create_test_game

def test_shuffle_deck(db_session):
    """Test deck shuffling functionality"""
    # Create game and cards first
    game = create_test_game(db_session)
    
    # Create actual Card records first
    for i in range(1, 6):
        create_test_card(db_session, i)
        create_card_in_db(db_session, i, position=i)
    
    service = GameCardsRepository(db_session)
    shuffled = service.shuffle_deck(game.id)
    
    # Verify we got cards back and positions changed
    assert len(shuffled) == 5
    positions = [c.position for c in shuffled]
    # Positions should be a permutation of 1-5
    assert set(positions) == {1, 2, 3, 4, 5}
    assert len(positions) == len(set(positions))  # All positions unique

def test_draw_from_deck(db_session):
    """Test drawing cards from deck"""
    game = create_test_game(db_session)
    
    # Create cards
    for i in range(1, 4):
        create_test_card(db_session, i)
        create_card_in_db(db_session, i, position=i)
    
    service = GameCardsRepository(db_session)
    drawn = service.draw_from_deck(game.id, 2)
    
    assert len(drawn) == 2
    assert all(c.location == CardLocation.HAND for c in drawn)
    
    # Check remaining cards in deck
    remaining_cards = db_session.query(GameCards).filter(
        GameCards.game_id == 1,
        GameCards.location == CardLocation.DECK
    ).all()
    assert len(remaining_cards) == 1

def test_assign_cards_to_player(db_session):
    """Test assigning cards to a player"""
    game = create_test_game(db_session)
    
    # Create cards in hand
    cards = []
    for i in range(1, 4):
        create_test_card(db_session, i)
        card = create_card_in_db(db_session, i, location=CardLocation.HAND)
        cards.append(card)
    
    service = GameCardsRepository(db_session)
    updated = service.assign_cards_to_player(cards, player_id=42)
    
    assert len(updated) == 3
    assert all(c.owner_id == 42 for c in updated)

def test_get_player_cards_in_hand(db_session):
    """Test getting player's hand count"""
    game = create_test_game(db_session)
    
    birthdate = datetime.strptime("2025-12-12", "%Y-%m-%d")
    # Create player
    player = Player(id=1, game_id=1, name="Test Player", birthdate=birthdate, turn=1)
    db_session.add(player)
    db_session.commit()
    
    # Create cards for player
    for i in range(1, 4):
        create_test_card(db_session, i)
        create_card_in_db(db_session, i, location=CardLocation.HAND, owner_id=1)
    
    service = GameCardsRepository(db_session)
    count = service.get_player_cards_in_hand(player_id=1)
    assert count == 3

def test_deal_initial(db_session):
    """Test dealing initial cards to players"""
    # Create game
    game = create_test_game(db_session)
    
    birthdate = datetime.strptime("2025-12-12", "%Y-%m-%d")

    # Create players with all required fields
    players = [
        Player(id=1, game_id=1, name="Player 1", birthdate=birthdate, turn=1),
        Player(id=2, game_id=1, name="Player 2", birthdate=birthdate, turn=2)
    ]
    db_session.add_all(players)
    db_session.commit()
    
    # Create cards
    for i in range(1, 5):
        create_test_card(db_session, i)
        create_card_in_db(db_session, i)
    
    service = GameCardsRepository(db_session)
    service.deal_initial(1, players, per_player=2)
    
    # Check each player has 2 cards
    for player in players:
        hand_count = service.get_player_cards_in_hand(player.id)
        assert hand_count == 2