import pytest
from fastapi import status
from unittest.mock import patch, AsyncMock
from models.pending_action_model import PendingAction, ActionType, ActionStatus
from models.counter_model import Counter
from models.game_cards_model import GameCards, CardLocation
from models.card_model import Card, CardType
from datetime import datetime, timedelta, timezone


@pytest.mark.asyncio
async def test_play_counter_success(test_client, db_session, started_game, seed_cards):
    """Test successfully playing a 'Not So Fast' counter card"""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2 = started_game["player2"]
    
    # Create a NSF card in player2's hand
    nsf_card_base = Card(image="nsf.png", type=CardType.NSF)
    db_session.add(nsf_card_base)
    db_session.flush()
    
    nsf_game_card = GameCards(
        game_id=game_id,
        card_id=nsf_card_base.id,
        owner_id=player2.id,
        location=CardLocation.HAND
    )
    db_session.add(nsf_game_card)
    db_session.commit()
    db_session.refresh(nsf_game_card)
    
    # Create a pending action from creator
    pending_action = PendingAction(
        game_id=game_id,
        action_type=ActionType.PLAY_SET.value,
        status=ActionStatus.PENDING.value,
        initiator_player_id=creator_id,
        action_payload={"set_id": 1},
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(seconds=10)
    )
    db_session.add(pending_action)
    db_session.commit()
    db_session.refresh(pending_action)
    
    # Mock the socket emission
    with patch("services.action_queue_service.sio.emit", new_callable=AsyncMock) as mock_emit:
        response = test_client.post(
            f"/games/{game_id}/actions/{pending_action.id}/counter",
            json={
                "player_id": player2.id,
                "card_id": nsf_game_card.id
            }
        )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert "counter_id" in data
    assert "chain_position" in data
    assert data["chain_position"] == 1
    assert "new_expires_at" in data
    assert "message" in data
    
    # Verify the NSF card was moved to discard pile
    db_session.refresh(nsf_game_card)
    assert nsf_game_card.location == CardLocation.DISCARD
    assert nsf_game_card.owner_id is None
    assert nsf_game_card.discard_order is not None
    
    # Verify counter was created
    counter = db_session.query(Counter).filter(Counter.action_id == pending_action.id).first()
    assert counter is not None
    assert counter.player_id == player2.id
    assert counter.nsf_game_card_id == nsf_game_card.id
    assert counter.chain_position == 1


@pytest.mark.asyncio
async def test_play_counter_missing_player_id(test_client, db_session, seed_cards, started_game):
    """Test counter play fails when player_id is missing"""
    game_id = started_game["game_id"]
    action_id = 1
    
    response = test_client.post(
        f"/games/{game_id}/actions/{action_id}/counter",
        json={
            "card_id": 10
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "player_id and card_id are required" in response.json()["detail"]


@pytest.mark.asyncio
async def test_play_counter_missing_card_id(test_client, db_session, seed_cards, started_game):
    """Test counter play fails when card_id is missing"""
    game_id = started_game["game_id"]
    action_id = 1
    player_id = 2
    
    response = test_client.post(
        f"/games/{game_id}/actions/{action_id}/counter",
        json={
            "player_id": player_id
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "player_id and card_id are required" in response.json()["detail"]


@pytest.mark.asyncio
async def test_play_counter_action_not_found(test_client, db_session, seed_cards, started_game):
    """Test counter play fails when action doesn't exist"""
    game_id = started_game["game_id"]
    action_id = 9999
    player2 = started_game["player2"]
    
    response = test_client.post(
        f"/games/{game_id}/actions/{action_id}/counter",
        json={
            "player_id": player2.id,
            "card_id": 10
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Action not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_play_counter_card_not_found(test_client, db_session, seed_cards, started_game):
    """Test counter play fails when NSF card doesn't exist"""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2 = started_game["player2"]
    
    # Create a pending action
    pending_action = PendingAction(
        game_id=game_id,
        action_type=ActionType.PLAY_SET.value,
        status=ActionStatus.PENDING.value,
        initiator_player_id=creator_id,
        action_payload={"set_id": 1},
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(seconds=10)
    )
    db_session.add(pending_action)
    db_session.commit()
    db_session.refresh(pending_action)
    
    response = test_client.post(
        f"/games/{game_id}/actions/{pending_action.id}/counter",
        json={
            "player_id": player2.id,
            "card_id": 9999
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "NSF card not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_play_counter_card_not_in_hand(test_client, db_session, seed_cards, started_game):
    """Test counter play fails when NSF card is not in player's hand"""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2 = started_game["player2"]
    
    # Create a NSF card in deck (not in hand)
    nsf_card_base = Card(image="nsf.png", type=CardType.NSF)
    db_session.add(nsf_card_base)
    db_session.flush()
    
    nsf_game_card = GameCards(
        game_id=game_id,
        card_id=nsf_card_base.id,
        owner_id=player2.id,
        location=CardLocation.DECK  # Not in hand!
    )
    db_session.add(nsf_game_card)
    db_session.commit()
    db_session.refresh(nsf_game_card)
    
    # Create a pending action
    pending_action = PendingAction(
        game_id=game_id,
        action_type=ActionType.PLAY_SET.value,
        status=ActionStatus.PENDING.value,
        initiator_player_id=creator_id,
        action_payload={"set_id": 1},
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(seconds=10)
    )
    db_session.add(pending_action)
    db_session.commit()
    db_session.refresh(pending_action)
    
    response = test_client.post(
        f"/games/{game_id}/actions/{pending_action.id}/counter",
        json={
            "player_id": player2.id,
            "card_id": nsf_game_card.id
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "NSF card is not in player's hand" in response.json()["detail"]


@pytest.mark.asyncio
async def test_play_counter_card_not_nsf_type(test_client, db_session, seed_cards, started_game):
    """Test counter play fails when card is not a 'Not So Fast' card"""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2 = started_game["player2"]
    
    # Create a different card type in player2's hand
    event_card_base = Card(image="event.png", type=CardType.EVT)
    db_session.add(event_card_base)
    db_session.flush()
    
    event_game_card = GameCards(
        game_id=game_id,
        card_id=event_card_base.id,
        owner_id=player2.id,
        location=CardLocation.HAND
    )
    db_session.add(event_game_card)
    db_session.commit()
    db_session.refresh(event_game_card)
    
    # Create a pending action
    pending_action = PendingAction(
        game_id=game_id,
        action_type=ActionType.PLAY_SET.value,
        status=ActionStatus.PENDING.value,
        initiator_player_id=creator_id,
        action_payload={"set_id": 1},
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(seconds=10)
    )
    db_session.add(pending_action)
    db_session.commit()
    db_session.refresh(pending_action)
    
    response = test_client.post(
        f"/games/{game_id}/actions/{pending_action.id}/counter",
        json={
            "player_id": player2.id,
            "card_id": event_game_card.id
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Card is not a 'Not So Fast' card" in response.json()["detail"]


@pytest.mark.asyncio
async def test_play_counter_card_not_owned_by_player(test_client, db_session, seed_cards, started_game):
    """Test counter play fails when NSF card doesn't belong to the player"""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2 = started_game["player2"]
    
    # Create a NSF card owned by creator (not player2)
    nsf_card_base = Card(image="nsf.png", type=CardType.NSF)
    db_session.add(nsf_card_base)
    db_session.flush()
    
    nsf_game_card = GameCards(
        game_id=game_id,
        card_id=nsf_card_base.id,
        owner_id=creator_id,  # Owned by creator, not player2
        location=CardLocation.HAND
    )
    db_session.add(nsf_game_card)
    db_session.commit()
    db_session.refresh(nsf_game_card)
    
    # Create a pending action
    pending_action = PendingAction(
        game_id=game_id,
        action_type=ActionType.PLAY_SET.value,
        status=ActionStatus.PENDING.value,
        initiator_player_id=creator_id,
        action_payload={"set_id": 1},
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(seconds=10)
    )
    db_session.add(pending_action)
    db_session.commit()
    db_session.refresh(pending_action)
    
    response = test_client.post(
        f"/games/{game_id}/actions/{pending_action.id}/counter",
        json={
            "player_id": player2.id,
            "card_id": nsf_game_card.id
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "NSF card does not belong to player" in response.json()["detail"]


@pytest.mark.asyncio
async def test_play_counter_cannot_counter_own_action(test_client, db_session, started_game, seed_cards):
    """Test that a player cannot counter their own action"""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    
    # Create a NSF card in creator's hand
    nsf_card_base = Card(image="nsf.png", type=CardType.NSF)
    db_session.add(nsf_card_base)
    db_session.flush()
    
    nsf_game_card = GameCards(
        game_id=game_id,
        card_id=nsf_card_base.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(nsf_game_card)
    db_session.commit()
    db_session.refresh(nsf_game_card)
    
    # Create a pending action initiated by creator
    pending_action = PendingAction(
        game_id=game_id,
        action_type=ActionType.PLAY_SET.value,
        status=ActionStatus.PENDING.value,
        initiator_player_id=creator_id,  # Initiated by creator
        action_payload={"set_id": 1},
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(seconds=10)
    )
    db_session.add(pending_action)
    db_session.commit()
    db_session.refresh(pending_action)
    
    response = test_client.post(
        f"/games/{game_id}/actions/{pending_action.id}/counter",
        json={
            "player_id": creator_id,  # Creator trying to counter their own action
            "card_id": nsf_game_card.id
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Cannot counter your own action" in response.json()["detail"]


@pytest.mark.asyncio
async def test_play_counter_expired_window(test_client, db_session, started_game, seed_cards):
    """Test counter play fails when the counter window has expired"""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2 = started_game["player2"]
    
    # Create a NSF card in player2's hand
    nsf_card_base = Card(image="nsf.png", type=CardType.NSF)
    db_session.add(nsf_card_base)
    db_session.flush()
    
    nsf_game_card = GameCards(
        game_id=game_id,
        card_id=nsf_card_base.id,
        owner_id=player2.id,
        location=CardLocation.HAND
    )
    db_session.add(nsf_game_card)
    db_session.commit()
    db_session.refresh(nsf_game_card)
    
    # Create an expired pending action
    pending_action = PendingAction(
        game_id=game_id,
        action_type=ActionType.PLAY_SET.value,
        status=ActionStatus.PENDING.value,
        initiator_player_id=creator_id,
        action_payload={"set_id": 1},
        created_at=datetime.utcnow() - timedelta(seconds=20),
        expires_at=datetime.utcnow() - timedelta(seconds=5)  # Expired!
    )
    db_session.add(pending_action)
    db_session.commit()
    db_session.refresh(pending_action)
    
    response = test_client.post(
        f"/games/{game_id}/actions/{pending_action.id}/counter",
        json={
            "player_id": player2.id,
            "card_id": nsf_game_card.id
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Counter window has expired" in response.json()["detail"]


@pytest.mark.asyncio
async def test_play_counter_action_wrong_game(test_client, db_session, seed_cards, started_game):
    """Test counter play fails when action belongs to a different game"""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2 = started_game["player2"]
    wrong_game_id = game_id + 100
    
    # Create a NSF card in player2's hand
    nsf_card_base = Card(image="nsf.png", type=CardType.NSF)
    db_session.add(nsf_card_base)
    db_session.flush()
    
    nsf_game_card = GameCards(
        game_id=game_id,
        card_id=nsf_card_base.id,
        owner_id=player2.id,
        location=CardLocation.HAND
    )
    db_session.add(nsf_game_card)
    db_session.commit()
    db_session.refresh(nsf_game_card)
    
    # Create a pending action for a different game
    pending_action = PendingAction(
        game_id=wrong_game_id,  # Different game!
        action_type=ActionType.PLAY_SET.value,
        status=ActionStatus.PENDING.value,
        initiator_player_id=creator_id,
        action_payload={"set_id": 1},
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(seconds=10)
    )
    db_session.add(pending_action)
    db_session.commit()
    db_session.refresh(pending_action)
    
    response = test_client.post(
        f"/games/{game_id}/actions/{pending_action.id}/counter",
        json={
            "player_id": player2.id,
            "card_id": nsf_game_card.id
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Action does not belong to this game" in response.json()["detail"]


@pytest.mark.asyncio
async def test_play_counter_action_not_counterable_status(test_client, db_session, seed_cards, started_game):
    """Test counter play fails when action status is not counterable (already resolved/cancelled)"""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2 = started_game["player2"]
    
    # Create a NSF card in player2's hand
    nsf_card_base = Card(image="nsf.png", type=CardType.NSF)
    db_session.add(nsf_card_base)
    db_session.flush()
    
    nsf_game_card = GameCards(
        game_id=game_id,
        card_id=nsf_card_base.id,
        owner_id=player2.id,
        location=CardLocation.HAND
    )
    db_session.add(nsf_game_card)
    db_session.commit()
    db_session.refresh(nsf_game_card)
    
    # Create a pending action that's already resolved
    pending_action = PendingAction(
        game_id=game_id,
        action_type=ActionType.PLAY_SET.value,
        status=ActionStatus.RESOLVED.value,  # Already resolved!
        initiator_player_id=creator_id,
        action_payload={"set_id": 1},
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(seconds=10)
    )
    db_session.add(pending_action)
    db_session.commit()
    db_session.refresh(pending_action)
    
    response = test_client.post(
        f"/games/{game_id}/actions/{pending_action.id}/counter",
        json={
            "player_id": player2.id,
            "card_id": nsf_game_card.id
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Action is no longer counterable" in response.json()["detail"]


@pytest.mark.asyncio
async def test_play_counter_multiple_counters_chain(test_client, db_session, started_game, seed_cards):
    """Test that multiple counters can be played creating a chain"""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2 = started_game["player2"]
    
    # Create NSF cards for both players
    nsf_card_base1 = Card(image="nsf1.png", type=CardType.NSF)
    db_session.add(nsf_card_base1)
    db_session.flush()
    
    nsf_game_card1 = GameCards(
        game_id=game_id,
        card_id=nsf_card_base1.id,
        owner_id=player2.id,
        location=CardLocation.HAND
    )
    db_session.add(nsf_game_card1)
    
    nsf_card_base2 = Card(image="nsf2.png", type=CardType.NSF)
    db_session.add(nsf_card_base2)
    db_session.flush()
    
    nsf_game_card2 = GameCards(
        game_id=game_id,
        card_id=nsf_card_base2.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(nsf_game_card2)
    db_session.commit()
    db_session.refresh(nsf_game_card1)
    db_session.refresh(nsf_game_card2)
    
    # Create a pending action
    pending_action = PendingAction(
        game_id=game_id,
        action_type=ActionType.PLAY_SET.value,
        status=ActionStatus.PENDING.value,
        initiator_player_id=creator_id,
        action_payload={"set_id": 1},
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(seconds=10)
    )
    db_session.add(pending_action)
    db_session.commit()
    db_session.refresh(pending_action)
    
    # Mock socket emissions
    with patch("services.action_queue_service.sio.emit", new_callable=AsyncMock):
        # First counter by player2
        response1 = test_client.post(
            f"/games/{game_id}/actions/{pending_action.id}/counter",
            json={
                "player_id": player2.id,
                "card_id": nsf_game_card1.id
            }
        )
        
        assert response1.status_code == status.HTTP_200_OK
        data1 = response1.json()
        assert data1["chain_position"] == 1
        
        # Refresh the action to get updated expires_at
        db_session.refresh(pending_action)
        
        # Second counter by creator (counter-countering player2)
        response2 = test_client.post(
            f"/games/{game_id}/actions/{pending_action.id}/counter",
            json={
                "player_id": creator_id,
                "card_id": nsf_game_card2.id
            }
        )
        
        assert response2.status_code == status.HTTP_200_OK
        data2 = response2.json()
        assert data2["chain_position"] == 2
    
    # Verify both counters exist in the database
    counters = db_session.query(Counter).filter(Counter.action_id == pending_action.id).all()
    assert len(counters) == 2
    assert counters[0].chain_position == 1
    assert counters[1].chain_position == 2


@pytest.mark.asyncio
async def test_play_counter_cannot_counter_own_counter(test_client, db_session, started_game, seed_cards):
    """Test that a player cannot counter their own counter (consecutive counters)"""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2 = started_game["player2"]
    
    # Create NSF cards for player2
    nsf_card_base1 = Card(image="nsf1.png", type=CardType.NSF)
    db_session.add(nsf_card_base1)
    db_session.flush()
    
    nsf_game_card1 = GameCards(
        game_id=game_id,
        card_id=nsf_card_base1.id,
        owner_id=player2.id,
        location=CardLocation.HAND
    )
    db_session.add(nsf_game_card1)
    
    nsf_card_base2 = Card(image="nsf2.png", type=CardType.NSF)
    db_session.add(nsf_card_base2)
    db_session.flush()
    
    nsf_game_card2 = GameCards(
        game_id=game_id,
        card_id=nsf_card_base2.id,
        owner_id=player2.id,
        location=CardLocation.HAND
    )
    db_session.add(nsf_game_card2)
    db_session.commit()
    db_session.refresh(nsf_game_card1)
    db_session.refresh(nsf_game_card2)
    
    # Create a pending action initiated by creator
    pending_action = PendingAction(
        game_id=game_id,
        action_type=ActionType.PLAY_SET.value,
        status=ActionStatus.PENDING.value,
        initiator_player_id=creator_id,
        action_payload={"set_id": 1},
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(seconds=10)
    )
    db_session.add(pending_action)
    db_session.commit()
    db_session.refresh(pending_action)
    
    # Mock socket emissions
    with patch("services.action_queue_service.sio.emit", new_callable=AsyncMock):
        # First counter by player2
        response1 = test_client.post(
            f"/games/{game_id}/actions/{pending_action.id}/counter",
            json={
                "player_id": player2.id,
                "card_id": nsf_game_card1.id
            }
        )
        
        assert response1.status_code == status.HTTP_200_OK
        
        # Attempt to counter again with player2 (should fail)
        response2 = test_client.post(
            f"/games/{game_id}/actions/{pending_action.id}/counter",
            json={
                "player_id": player2.id,
                "card_id": nsf_game_card2.id
            }
        )
        
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "Cannot counter your own counter" in response2.json()["detail"]
