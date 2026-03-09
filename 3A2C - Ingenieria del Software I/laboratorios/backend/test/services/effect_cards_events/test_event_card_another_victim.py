"""Tests for another_victim endpoint and play_another_victim method."""

import pytest
from fastapi import status, HTTPException
from models.card_model import Card, CardType
from models.game_cards_model import GameCards as GameCardsModel, CardLocation
from services.effect_cards_events import CardsEventsEffects
from repositories.set_repository import SetRepository
from repositories.game_cards_repository import GameCardsRepository
from models.set_model import SetPlay


@pytest.mark.asyncio
async def test_play_another_victim_success(db_session, create_game_with_players_and_sets, seed_cards):
    """
    Test successful execution of another victim card.
    Verifies the card is discarded and the set is NOT stolen.
    """
    game_id = create_game_with_players_and_sets["game_id"]
    creator_id = create_game_with_players_and_sets["creator_id"]
    player2_id = create_game_with_players_and_sets["player2_id"]

    
    target_set_id = next(s["set_id"] for s in create_game_with_players_and_sets["sets"] if s["type"] == "MR_SATTERTHWAITE" and s["owner_id"] == player2_id)

    
    event_card = Card(image="another_victim.png", type=CardType.EVT)
    db_session.add(event_card)
    db_session.commit()
    db_session.refresh(event_card)

    gc = GameCardsModel(
        game_id=game_id,
        card_id=event_card.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(gc)
    db_session.commit()
    db_session.refresh(gc)

    service = CardsEventsEffects(db_session)
   
    
    result = await service.play_another_victim(
        game_id=game_id,
        player_id=creator_id,
        event_card_id=gc.id,
        target_set_id=target_set_id,
    )

    
    set_repo = SetRepository(db_session)
    updated_set = set_repo.get_by_id(target_set_id)
    assert updated_set.owner_id == player2_id  # El propietario DEBE seguir siendo player2

    
    gc_repo = GameCardsRepository(db_session)
    discarded_gc = gc_repo.get_card_by_id(gc.id)
    assert discarded_gc.location == CardLocation.DISCARD
    assert discarded_gc.owner_id is None

    
    assert isinstance(result, SetPlay)
    assert result.id == target_set_id
    assert result.owner_id == player2_id

@pytest.mark.asyncio
async def test_play_another_victim_target_own_set(db_session, create_game_with_players_and_sets, seed_cards):
    """
    Test targeting own set.
    The method should execute successfully (discarding the card) 
    as the new logic doesn't prevent it.
    """
    game_id = create_game_with_players_and_sets["game_id"]
    creator_id = create_game_with_players_and_sets["creator_id"]


    own_set_id = next(s["set_id"] for s in create_game_with_players_and_sets["sets"] if s["type"] == "HERCULE_POIROT" and s["owner_id"] == creator_id)


    event_card = Card(image="another_victim.png", type=CardType.EVT)
    db_session.add(event_card)
    db_session.commit()
    db_session.refresh(event_card)

    gc = GameCardsModel(
        game_id=game_id,
        card_id=event_card.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(gc)
    db_session.commit()
    db_session.refresh(gc)

    service = CardsEventsEffects(db_session)
    

    result = await service.play_another_victim(
        game_id=game_id,
        player_id=creator_id,
        event_card_id=gc.id,
        target_set_id=own_set_id,
    )


    gc_repo = GameCardsRepository(db_session)
    discarded_gc = gc_repo.get_card_by_id(gc.id)
    assert discarded_gc.location == CardLocation.DISCARD


    set_repo = SetRepository(db_session)
    updated_set = set_repo.get_by_id(own_set_id)
    assert updated_set.owner_id == creator_id
    assert result.owner_id == creator_id


@pytest.mark.asyncio
async def test_play_another_victim_card_not_found(db_session, create_game_with_players_and_sets, seed_cards):
    """Test with non-existent card."""
    game_id = create_game_with_players_and_sets["game_id"]
    creator_id = create_game_with_players_and_sets["creator_id"]
    player2_id = create_game_with_players_and_sets["player2_id"]
    
    target_set_id = next(s["set_id"] for s in create_game_with_players_and_sets["sets"] if s["type"] == "PARKER_PYNE" and s["owner_id"] == player2_id)

    service = CardsEventsEffects(db_session)
    with pytest.raises(HTTPException) as excinfo:

        await service.play_another_victim(
            game_id=game_id,
            player_id=creator_id,
            event_card_id=99999, 
            target_set_id=target_set_id,
        )
    assert excinfo.value.status_code == status.HTTP_404_NOT_FOUND
    assert "card not found" in str(excinfo.value.detail).lower()


@pytest.mark.asyncio
async def test_play_another_victim_card_not_owned(db_session, create_game_with_players_and_sets, seed_cards):
    """Test with card owned by another player."""
    game_id = create_game_with_players_and_sets["game_id"]
    creator_id = create_game_with_players_and_sets["creator_id"]
    player2_id = create_game_with_players_and_sets["player2_id"]
    
    target_set_id = next(s["set_id"] for s in create_game_with_players_and_sets["sets"] if s["type"] == "PARKER_PYNE" and s["owner_id"] == player2_id)

    
    event_card = Card(image="another_victim.png", type=CardType.EVT)
    db_session.add(event_card)
    db_session.commit()
    db_session.refresh(event_card)

    gc = GameCardsModel(
        game_id=game_id,
        card_id=event_card.id,
        owner_id=player2_id, 
        location=CardLocation.HAND
    )
    db_session.add(gc)
    db_session.commit()
    db_session.refresh(gc)

    service = CardsEventsEffects(db_session)
    with pytest.raises(HTTPException) as excinfo:
        # Llamada actualizada
        await service.play_another_victim(
            game_id=game_id,
            player_id=creator_id,
            event_card_id=gc.id,
            target_set_id=target_set_id,
        )
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "not yours" in str(excinfo.value.detail).lower()


@pytest.mark.asyncio
async def test_play_another_victim_invalid_set(db_session, create_game_with_players_and_sets, seed_cards):
    """Test with non-existent set."""
    game_id = create_game_with_players_and_sets["game_id"]
    creator_id = create_game_with_players_and_sets["creator_id"]

    
    event_card = Card(image="another_victim.png", type=CardType.EVT)
    db_session.add(event_card)
    db_session.commit()
    db_session.refresh(event_card)

    gc = GameCardsModel(
        game_id=game_id,
        card_id=event_card.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(gc)
    db_session.commit()
    db_session.refresh(gc)

    service = CardsEventsEffects(db_session)
    with pytest.raises(HTTPException) as excinfo:

        await service.play_another_victim(
            game_id=game_id,
            player_id=creator_id,
            event_card_id=gc.id,
            target_set_id=99999,  # ID de set no existente
        )

    assert excinfo.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "target_set_id" in str(excinfo.value.detail).lower()


@pytest.mark.asyncio
async def test_endpoint_another_victim_success(test_client, db_session, create_game_with_players_and_sets, seed_cards):
    """Test endpoint with valid request."""
    game_id = create_game_with_players_and_sets["game_id"]
    creator_id = create_game_with_players_and_sets["creator_id"]
    player2_id = create_game_with_players_and_sets["player2_id"] 


    target_set_id = next(s["set_id"] for s in create_game_with_players_and_sets["sets"] if s["type"] == "PARKER_PYNE" and s["owner_id"] == player2_id)
    

    event_card = Card(image="another_victim.png", type=CardType.EVT)
    db_session.add(event_card)
    db_session.commit()
    db_session.refresh(event_card)

    gc = GameCardsModel(
        game_id=game_id,
        card_id=event_card.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(gc)
    db_session.commit()
    db_session.refresh(gc)



    request_data = {
        "event_card_id": gc.id,
        "set_id": target_set_id 
    }

 
    response = test_client.post(
        f"/games/play/another_victim/{game_id}/{creator_id}",
        json=request_data
    )


    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "success"


    set_repo = SetRepository(db_session)
    updated_set = set_repo.get_by_id(target_set_id)
    assert updated_set.owner_id == player2_id


@pytest.mark.asyncio
async def test_endpoint_another_victim_invalid_card(test_client, db_session, create_game_with_players_and_sets, seed_cards):
    """Test endpoint with invalid card."""
    game_id = create_game_with_players_and_sets["game_id"]
    creator_id = create_game_with_players_and_sets["creator_id"]
    player2_id = create_game_with_players_and_sets["player2_id"] 
    
    target_set_id = next(s["set_id"] for s in create_game_with_players_and_sets["sets"] if s["type"] == "PARKER_PYNE" and s["owner_id"] == player2_id)

    request_data = {
        "event_card_id": 99999, 
        "set_id": target_set_id 
    }

    response = test_client.post(
        f"/games/play/another_victim/{game_id}/{creator_id}",
        json=request_data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "card not found" in response.json()["detail"].lower()