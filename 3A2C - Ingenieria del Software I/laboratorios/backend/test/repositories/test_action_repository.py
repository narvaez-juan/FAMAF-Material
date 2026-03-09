import pytest
from datetime import datetime

from repositories.action_repository import ActionRepository
from models.pending_action_model import ActionType, ActionStatus


@pytest.mark.asyncio
async def test_create_pending_action_and_get_by_id(db_session, create_game_with_players):
    """Create a pending action using the game/player"""
    game_data = create_game_with_players
    game_id = game_data["game_id"]
    creator_id = game_data["creator_id"]

    repo = ActionRepository(db_session)

    payload = {"some": "data"}
    action = repo.create_pending_action(
        game_id=game_id,
        action_type=ActionType.PLAY_SET,
        initiator_player_id=creator_id,
        action_payload=payload,
        countdown_seconds=30,
    )

    assert action is not None
    assert action.action_payload == payload
    assert action.status == ActionStatus.PENDING.value


@pytest.mark.asyncio
async def test_add_counter_and_get_counters_for_action(db_session, create_game_with_players, create_player2_card):
    """Use fixtures to get a game with players and a game card assigned to player2"""
    game_data = create_game_with_players
    game_id = game_data["game_id"]
    creator_id = game_data["creator_id"]
    player2 = game_data["player2"]

    nsf_game_card = create_player2_card

    repo = ActionRepository(db_session)

    action = repo.create_pending_action(
        game_id=game_id,
        action_type=ActionType.STEAL_SECRET,
        initiator_player_id=creator_id,
        action_payload={"target": player2.id},
        countdown_seconds=30,
    )

    counter1 = repo.add_counter(action.id, player_id=player2.id, nsf_game_card_id=nsf_game_card.id)
    assert counter1.chain_position == 1

    counter2 = repo.add_counter(action.id, player_id=creator_id, nsf_game_card_id=nsf_game_card.id)
    assert counter2.chain_position == 2

    refreshed = repo.get_by_id(action.id)
    assert refreshed.status == ActionStatus.COUNTER_PENDING.value

    counters = repo.get_counters_for_action(action.id)
    assert len(counters) == 2
    assert [c.chain_position for c in counters] == [1, 2]


@pytest.mark.asyncio
async def test_get_expired_actions_and_resolve_action(db_session, create_game_with_players):
    """Should find expired actions and allow resolving them"""
    game_data = create_game_with_players
    game_id = game_data["game_id"]
    creator_id = game_data["creator_id"]

    repo = ActionRepository(db_session)

    expired_action = repo.create_pending_action(
        game_id=game_id,
        action_type=ActionType.PLAY_SET,
        initiator_player_id=creator_id,
        action_payload={"a": 1},
        countdown_seconds=-10,
    )

    expired = repo.get_expired_actions()
    assert any(a.id == expired_action.id for a in expired)

    repo.resolve_action(expired_action.id, ActionStatus.RESOLVED)
    resolved = repo.get_by_id(expired_action.id)
    assert resolved.status == ActionStatus.RESOLVED.value
