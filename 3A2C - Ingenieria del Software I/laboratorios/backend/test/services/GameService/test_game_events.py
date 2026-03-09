import sys
from pathlib import Path


# NOTE - HATE HATE HATE PAHT
root = Path(__file__).resolve().parents[1]
src = root / "src"
sys.path.insert(0, str(src))

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy.orm import Session
from schemas.game_schema import GameFinishReason
from fastapi import HTTPException

from services.game_events import (
    emit_game_list,
    emit_game_start,
    emit_player_joined,
    emit_game_info,
    emit_game_finished,
)


@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_sio_emit():
    with patch("services.game_events.sio.emit", new_callable=AsyncMock) as mock_emit:
        yield mock_emit


@pytest.mark.asyncio
async def test_emit_game_list_emits_game_list(mock_db_session, mock_sio_emit):
    g1 = MagicMock()
    g1.id = 1
    g1.name = "G1"
    g1.players_amount = 2
    g1.max_players = 4
    g2 = MagicMock()
    g2.id = 2
    g2.name = "G2"
    g2.players_amount = 1
    g2.max_players = 6

    mock_repo = MagicMock()
    mock_repo.get_games.return_value = [g1, g2]

    with patch("services.game_events.GameRepository") as MockGameRepo:
        MockGameRepo.return_value = mock_repo

        await emit_game_list(mock_db_session)

    expected = [
        {"id": 1, "name": "G1", "currentPlayers": 2, "maxPlayers": 4},
        {"id": 2, "name": "G2", "currentPlayers": 1, "maxPlayers": 6},
    ]
    mock_sio_emit.assert_awaited_once_with("game_list", expected, room="games:list")


@pytest.mark.asyncio
async def test_emit_game_start_in_success(mock_db_session, mock_sio_emit):
    mock_game = MagicMock()
    mock_game.id = 1
    mock_game.name = "game1"
    mock_game.players_amount = 1
    mock_game.max_players = 6
    mock_game.min_players = 2
    mock_game.in_game = False

    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = mock_game

    with patch("services.game_events.GameRepository") as MockGameRepo:
        MockGameRepo.return_value = mock_repo
        await emit_game_start(1, mock_db_session)

    expected_game_start = {"id": 1, "status": "started"}
    mock_sio_emit.assert_awaited_once_with(
        "game_started", expected_game_start, room="game:1"
    )


@pytest.mark.asyncio
async def test_emit_player_join_in_success(mock_db_session, mock_sio_emit):
    # Mock game with players_amount
    mock_game = MagicMock()
    mock_game.id = 1
    mock_game.players_amount = 3

    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = mock_game

    with patch("services.game_events.GameRepository") as MockGameRepo:
        MockGameRepo.return_value = mock_repo
        await emit_player_joined(1, "Pedernera", mock_db_session)

    expected_player_joined = {"playerName": "Pedernera", "currentPlayers": 3}
    mock_sio_emit.assert_awaited_once_with(
        "player_joined", expected_player_joined, room="game:1"
    )


@pytest.mark.asyncio
async def test_emit_game_info_in_success(mock_db_session, mock_sio_emit):
    # Mock game
    mock_game = MagicMock()
    mock_game.id = 1
    mock_game.name = "game1"
    mock_game.players_amount = 2
    mock_game.min_players = 2
    mock_game.max_players = 6
    mock_game.in_game = False
    mock_game.current_turn = 0

    # Mock players
    p1 = MagicMock()
    p1.id = 1
    p1.name = "JEREEEEE"
    p1.turn = 0
    p2 = MagicMock()
    p2.id = 2
    p2.name = "PINI"
    p2.turn = 1
    mock_players = [p1, p2]

    # Mock repo
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = mock_game
    mock_repo.get_players.return_value = mock_players

    with patch("services.game_events.GameRepository") as MockGameRepo:
        MockGameRepo.return_value = mock_repo
        await emit_game_info(1, mock_db_session)

    expected_payload = {
        "id": 1,
        "name": "game1",
        "currentPlayers": 2,
        "minPlayers": 2,
        "maxPlayers": 6,
        "status": False,
        "currentTurn": 0,
        "players": [
            {"player_id": 1, "name": "JEREEEEE", "playerTurn": 0},
            {"player_id": 2, "name": "PINI", "playerTurn": 1},
        ],
    }

    mock_sio_emit.assert_awaited_once_with("game_info", expected_payload, room="game:1")


@pytest.mark.asyncio
async def test_emit_game_finished_emits_correct_event_and_payload(
    mock_db_session, mock_sio_emit
):

    mock_game = MagicMock()
    mock_game.id = 42

    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = mock_game

    with patch("services.game_events.GameRepository") as MockGameRepo:
        MockGameRepo.return_value = mock_repo
        await emit_game_finished(42, 7, GameFinishReason.MURDERER_ESCAPES, mock_db_session)

    expected_payload = {
        "type": "game_finished",
        "payload": {"winner_id": 7, "reason": GameFinishReason.MURDERER_ESCAPES.value},
    }
    mock_sio_emit.assert_awaited_once_with(
        "notify_winner", expected_payload, room="game:42"
    )

@pytest.mark.asyncio
async def test_emit_game_finished_with_murderer_wins(
    mock_db_session, mock_sio_emit
):

    mock_game = MagicMock()
    mock_game.id = 99

    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = mock_game

    with patch("services.game_events.GameRepository") as MockGameRepo:
        MockGameRepo.return_value = mock_repo
        await emit_game_finished(99, 3, GameFinishReason.ALL_DETECTIVES_ELIMINATED, mock_db_session)

    expected_payload = {
        "type": "game_finished",
        "payload": {"winner_id": 3, "reason": GameFinishReason.ALL_DETECTIVES_ELIMINATED.value},
    }
    mock_sio_emit.assert_awaited_once_with(
        "notify_winner", expected_payload, room="game:99"
    )

@pytest.mark.asyncio
async def test_emit_game_finished_with_detectives_wins(
    mock_db_session, mock_sio_emit
):

    mock_game = MagicMock()
    mock_game.id = 55

    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = mock_game

    with patch("services.game_events.GameRepository") as MockGameRepo:
        MockGameRepo.return_value = mock_repo
        await emit_game_finished(55, 8, GameFinishReason.MURDERER_REVEALED, mock_db_session)

    expected_payload = {
        "type": "game_finished",
        "payload": {"winner_id": 8, "reason": GameFinishReason.MURDERER_REVEALED.value},
    }
    mock_sio_emit.assert_awaited_once_with(
        "notify_winner", expected_payload, room="game:55"
    )

@pytest.mark.asyncio
async def test_emit_game_finished_game_not_found_raises(mock_db_session):

    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = None

    with patch("services.game_events.GameRepository") as MockGameRepo:
        MockGameRepo.return_value = mock_repo
        with pytest.raises(HTTPException) as exc:
            await emit_game_finished(1, 1, GameFinishReason.MURDERER_ESCAPES, mock_db_session)
        assert exc.value.status_code == 404
        assert "Game not found" in str(exc.value.detail)
