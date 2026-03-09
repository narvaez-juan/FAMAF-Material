import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models.card_model import Card, CardType
from models.game_cards_model import GameCards, CardLocation
from models.game_model import Game
from models.player_model import Player
import datetime

from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
@patch("services.effect_cards_events.emit_player_hand", new_callable=AsyncMock)
@patch("services.effect_cards_events.emit_discard_pile", new_callable=AsyncMock)
@patch("services.effect_cards_events.emit_look_into_the_ashes_event", new_callable=AsyncMock)
async def test_play_look_into_the_ashes_success(
    mock_emit_ashes,
    mock_emit_discard,
    mock_emit_hand,
    test_client: TestClient, 
    db_session: Session, 
    create_game_with_players_and_sets,
    seed_cards,
):
    """
    Testea el caso de éxito de 'play_look_into_the_ashes'.
    Usa el patrón de fixtures de 'test_event_card_another_victim.py'.
    Usa unittest.mock en lugar de pytest-mock (mocker).
    """
    
    # --- ARRANGE (Given) ---
    game_id = create_game_with_players_and_sets["game_id"]
    player_id = create_game_with_players_and_sets["creator_id"]

    # Crear las cartas base (Card) necesarias
    look_into_ashes_base_card = Card(image="look_into_the_ashes.png", type=CardType.EVT)
    discarded_base_card = Card(image="discarded_card.png", type=CardType.DET)
    db_session.add_all([look_into_ashes_base_card, discarded_base_card])
    db_session.commit()
    db_session.refresh(look_into_ashes_base_card)
    db_session.refresh(discarded_base_card)

    # Crear la GameCard del evento en la mano del jugador
    event_game_card = GameCards(
        card_id=look_into_ashes_base_card.id,
        game_id=game_id,
        owner_id=player_id,
        location=CardLocation.HAND
    )
    db_session.add(event_game_card)
    db_session.commit()

    # Crear la GameCard descartada en la pila de descarte
    discarded_game_card = GameCards(
        card_id=discarded_base_card.id,
        game_id=game_id,
        owner_id=None,
        location=CardLocation.DISCARD,
        discard_order=1
    )
    db_session.add(discarded_game_card)
    db_session.flush()  # Asegurar que la carta se persista
    db_session.commit()
    db_session.refresh(event_game_card)
    db_session.refresh(discarded_game_card)
    
    assert discarded_game_card.discard_order == 1, f"discard_order should be 1, got {discarded_game_card.discard_order}"

    payload = {
        "event_card_id": event_game_card.id,
        "chosen_gamecard_id": discarded_game_card.id
    }
    
    response = test_client.post(
        f"/games/play/look-into-the-ashes/{game_id}/{player_id}",
        json=payload
    )
    
    assert response.status_code == 200, response.json()
    assert response.json() == {"status": "success"}

    db_session.refresh(event_game_card)
    db_session.refresh(discarded_game_card)

    assert event_game_card.location == CardLocation.DISCARD
    assert event_game_card.owner_id is None
    assert discarded_game_card.location == CardLocation.HAND
    assert discarded_game_card.owner_id == player_id

    mock_emit_ashes.assert_called_once()
    mock_emit_discard.assert_called_once()
    mock_emit_hand.assert_called_once()


@pytest.mark.asyncio
@patch("services.card_events.emit_player_hand", new_callable=AsyncMock)
@patch("services.card_events.emit_discard_pile", new_callable=AsyncMock)
@patch("services.card_events.emit_look_into_the_ashes_event", new_callable=AsyncMock)
async def test_play_look_into_the_ashes_fail_card_not_in_discard(
    mock_emit_ashes,
    mock_emit_discard,
    mock_emit_hand,
    test_client: TestClient, 
    db_session: Session, 
    create_game_with_players_and_sets,
    seed_cards,
):
    """
    Testea el caso de fallo cuando la 'chosen_gamecard_id' no se encuentra 
    entre las últimas 5 cartas del descarte.
    """
    
    # --- ARRANGE (Given) ---
    game_id = create_game_with_players_and_sets["game_id"]
    player_id = create_game_with_players_and_sets["creator_id"]

    # Crear carta de evento en la mano
    look_into_ashes_base_card = Card(image="look_into_the_ashes.png", type=CardType.EVT)
    db_session.add(look_into_ashes_base_card)
    db_session.commit()
    db_session.refresh(look_into_ashes_base_card)

    event_game_card = GameCards(
        card_id=look_into_ashes_base_card.id,
        game_id=game_id,
        owner_id=player_id,
        location=CardLocation.HAND
    )
    
    discarded_base_card = Card(image="discarded_card.png", type=CardType.DET)
    db_session.add(discarded_base_card)
    db_session.commit()
    db_session.refresh(discarded_base_card)

    discarded_game_card = GameCards(
        card_id=discarded_base_card.id,
        game_id=game_id,
        location=CardLocation.DISCARD,
        discard_order=1
    )
    db_session.add_all([event_game_card, discarded_game_card])
    db_session.commit()
    db_session.refresh(event_game_card)
    db_session.refresh(discarded_game_card)

    payload = {
        "event_card_id": event_game_card.id,
        "chosen_gamecard_id": 99999
    }
    
    response = test_client.post(
        f"/games/play/look-into-the-ashes/{game_id}/{player_id}",
        json=payload
    )

    assert response.status_code == 400
    assert "The chosen card is not among the last discarded cards" in response.json()["detail"]
    

    mock_emit_ashes.assert_not_called()
    mock_emit_discard.assert_not_called()
    mock_emit_hand.assert_not_called()


@pytest.mark.asyncio
@patch("services.card_events.emit_player_hand", new_callable=AsyncMock)
@patch("services.card_events.emit_discard_pile", new_callable=AsyncMock)
@patch("services.card_events.emit_look_into_the_ashes_event", new_callable=AsyncMock)
async def test_play_look_into_the_ashes_fail_no_discard_pile(
    mock_emit_ashes,
    mock_emit_discard,
    mock_emit_hand,
    test_client: TestClient, 
    db_session: Session, 
    create_game_with_players_and_sets,
    seed_cards,
):
    """
    Testea el caso de fallo cuando no hay cartas en la pila de descarte.
    """

    game_id = create_game_with_players_and_sets["game_id"]
    player_id = create_game_with_players_and_sets["creator_id"]

    look_into_ashes_base_card = Card(image="look_into_the_ashes.png", type=CardType.EVT)
    db_session.add(look_into_ashes_base_card)
    db_session.commit()
    db_session.refresh(look_into_ashes_base_card)

    event_game_card = GameCards(
        card_id=look_into_ashes_base_card.id,
        game_id=game_id,
        owner_id=player_id,
        location=CardLocation.HAND
    )
    db_session.add(event_game_card)
    db_session.commit()
    db_session.refresh(event_game_card)

    payload = {
        "event_card_id": event_game_card.id,
        "chosen_gamecard_id": 1
    }
    
    response = test_client.post(
        f"/games/play/look-into-the-ashes/{game_id}/{player_id}",
        json=payload
    )
    
    assert response.status_code == 400
    assert "There are no cards in the discard pile" in response.json()["detail"]
    
    mock_emit_ashes.assert_not_called()
    mock_emit_discard.assert_not_called()
    mock_emit_hand.assert_not_called()