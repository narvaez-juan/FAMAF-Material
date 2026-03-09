import enum
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
src = root / "src"
sys.path.insert(0, str(src))

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from services.action_queue_service import ActionQueueService, ActionCancelledException
from models.pending_action_model import PendingAction, ActionType, ActionStatus
from models.counter_model import Counter
from models.game_cards_model import CardLocation, GameCards
from models.card_model import CardType
from datetime import datetime, timedelta, timezone


@pytest.mark.asyncio
async def test_play_counter_success(action_queue_service, mock_action_repo, mock_game_cards_repo, mock_db_session, sample_pending_action, sample_nsf_card):
    """Test successful counter play"""
    action_id = 1
    player_id = 2
    nsf_game_card_id = 10
    game_id = 1

    mock_counter = MagicMock(spec=Counter)
    mock_counter.id = 1
    mock_counter.chain_position = 1

    mock_action_repo.get_by_id.return_value = sample_pending_action
    mock_game_cards_repo.get_by_id.return_value = sample_nsf_card
    mock_action_repo.add_counter.return_value = mock_counter
    mock_action_repo.get_counters_for_action.return_value = []  # No existing counters

    with patch.object(action_queue_service, '_emit_counter_played', new_callable=AsyncMock) as mock_emit:
        result = await action_queue_service.play_counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id,
            game_id=game_id
        )

        assert result["counter_id"] == 1
        assert result["chain_position"] == 1
        assert "new_expires_at" in result

        mock_action_repo.get_by_id.assert_called_once_with(action_id)
        mock_game_cards_repo.get_by_id.assert_called_once_with(nsf_game_card_id)
        mock_action_repo.add_counter.assert_called_once_with(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id
        )

        assert sample_nsf_card.location == CardLocation.DISCARD
        assert sample_nsf_card.owner_id is None
        assert sample_nsf_card.discard_order is not None

        mock_db_session.commit.assert_called_once()
        mock_emit.assert_called_once()


@pytest.mark.asyncio
async def test_play_counter_action_not_found(action_queue_service, mock_action_repo):
    """Test counter play when action doesn't exist"""
    action_id = 999
    player_id = 2
    nsf_game_card_id = 10
    game_id = 1

    mock_action_repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Action not found"):
        await action_queue_service.play_counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id,
            game_id=game_id
        )


@pytest.mark.asyncio
async def test_play_counter_wrong_game_id(action_queue_service, mock_action_repo, sample_pending_action):
    """Test counter play with wrong game ID"""
    action_id = 1
    player_id = 2
    nsf_game_card_id = 10
    game_id = 2 

    mock_action_repo.get_by_id.return_value = sample_pending_action

    with pytest.raises(ValueError, match="Action does not belong to this game"):
        await action_queue_service.play_counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id,
            game_id=game_id
        )


@pytest.mark.asyncio
async def test_play_counter_expired_action(action_queue_service, mock_action_repo, sample_pending_action):
    """Test counter play on expired action"""

    action_id = 1
    player_id = 2
    nsf_game_card_id = 10
    game_id = 1

    sample_pending_action.expires_at = datetime.utcnow() - timedelta(seconds=1)

    mock_action_repo.get_by_id.return_value = sample_pending_action

    with pytest.raises(ValueError, match="Counter window has expired"):
        await action_queue_service.play_counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id,
            game_id=game_id
        )


@pytest.mark.asyncio
async def test_play_counter_invalid_status(action_queue_service, mock_action_repo, sample_pending_action):
    """Test counter play on action with invalid status"""

    action_id = 1
    player_id = 2
    nsf_game_card_id = 10
    game_id = 1

    sample_pending_action.status = ActionStatus.RESOLVED

    mock_action_repo.get_by_id.return_value = sample_pending_action


    with pytest.raises(ValueError, match="Action is no longer counterable"):
        await action_queue_service.play_counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id,
            game_id=game_id
        )


@pytest.mark.asyncio
async def test_play_counter_card_not_found(action_queue_service, mock_action_repo, mock_game_cards_repo, sample_pending_action):
    """Test counter play with non-existent NSF card"""

    action_id = 1
    player_id = 2
    nsf_game_card_id = 999
    game_id = 1

    mock_action_repo.get_by_id.return_value = sample_pending_action
    mock_game_cards_repo.get_by_id.return_value = None


    with pytest.raises(ValueError, match="NSF card not found"):
        await action_queue_service.play_counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id,
            game_id=game_id
        )


@pytest.mark.asyncio
async def test_play_counter_wrong_card_owner(action_queue_service, mock_action_repo, mock_game_cards_repo, sample_pending_action, sample_nsf_card):
    """Test counter play with card owned by different player"""

    action_id = 1
    player_id = 3  
    nsf_game_card_id = 10
    game_id = 1

    mock_action_repo.get_by_id.return_value = sample_pending_action
    mock_game_cards_repo.get_by_id.return_value = sample_nsf_card

    with pytest.raises(ValueError, match="NSF card does not belong to player"):
        await action_queue_service.play_counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id,
            game_id=game_id
        )


@pytest.mark.asyncio
async def test_play_counter_card_not_in_hand(action_queue_service, mock_action_repo, mock_game_cards_repo, sample_pending_action, sample_nsf_card):
    """Test counter play with card not in hand"""

    action_id = 1
    player_id = 2
    nsf_game_card_id = 10
    game_id = 1


    sample_nsf_card.location = CardLocation.DISCARD

    mock_action_repo.get_by_id.return_value = sample_pending_action
    mock_game_cards_repo.get_by_id.return_value = sample_nsf_card


    with pytest.raises(ValueError, match="NSF card is not in player's hand"):
        await action_queue_service.play_counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id,
            game_id=game_id
        )


@pytest.mark.asyncio
async def test_play_counter_not_nsf_card(action_queue_service, mock_action_repo, mock_game_cards_repo, sample_pending_action, sample_nsf_card):
    """Test counter play with non-NSF card"""

    action_id = 1
    player_id = 2
    nsf_game_card_id = 10
    game_id = 1


    sample_nsf_card.card.type = CardType.EVT

    mock_action_repo.get_by_id.return_value = sample_pending_action
    mock_game_cards_repo.get_by_id.return_value = sample_nsf_card

    # Execute & Assert
    with pytest.raises(ValueError, match="Card is not a 'Not So Fast' card"):
        await action_queue_service.play_counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id,
            game_id=game_id
        )


@pytest.mark.asyncio
async def test_play_counter_initiator_cannot_counter(action_queue_service, mock_action_repo, mock_game_cards_repo, sample_pending_action):
    """Test that action initiator cannot counter their own action"""

    action_id = 1
    player_id = 1  
    nsf_game_card_id = 10
    game_id = 1

    initiator_card = MagicMock(spec=GameCards)
    initiator_card.id = 10
    initiator_card.owner_id = 1
    initiator_card.location = CardLocation.HAND
    initiator_card.card = MagicMock()
    initiator_card.card.type = CardType.NSF
    initiator_card.discard_order = None

    mock_action_repo.get_by_id.return_value = sample_pending_action
    mock_game_cards_repo.get_by_id.return_value = initiator_card
    mock_action_repo.get_counters_for_action.return_value = []  # No existing counters


    with pytest.raises(ValueError, match="Cannot counter your own action"):
        await action_queue_service.play_counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id,
            game_id=game_id
        )