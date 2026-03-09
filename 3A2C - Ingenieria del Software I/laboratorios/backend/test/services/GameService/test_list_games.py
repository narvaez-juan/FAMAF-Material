import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy.orm import Session

from services.game_events import emit_game_list
from models.game_model import Game


@pytest.fixture
def mock_db_session():
    db_session = MagicMock(spec=Session)
    return db_session


@pytest.fixture
def mock_sio():
    with patch("services.game_events.sio", new_callable=AsyncMock) as mock_sio:
        yield mock_sio

@pytest.mark.asyncio
async def test_emit_game_list_no_games(mock_db_session, mock_sio):
    # Configure the mock to return an empty list for the repository query
    mock_db_session.query.return_value.filter.return_value.all.return_value = []

    # Call the function
    await emit_game_list(mock_db_session)

    # Verify that the event was emitted with an empty list
    mock_sio.emit.assert_awaited_once_with("game_list", [], room="games:list")

@pytest.mark.asyncio
async def test_emit_game_list_with_games(mock_db_session, mock_sio):
    # Create mock game data
    mock_games = [
        Game(id=1, name="Game 1", players_amount=2, max_players=4),
        Game(id=2, name="Game 2", players_amount=3, max_players=5),
    ]

    # Configure the mock to return the mock games
    mock_db_session.query.return_value.filter.return_value.all.return_value = mock_games

    # Call the function
    await emit_game_list(mock_db_session)

    # Verify that the event was emitted with the correct game list
    expected_game_list = [
        {"id": 1, "name": "Game 1", "currentPlayers": 2, "maxPlayers": 4},
        {"id": 2, "name": "Game 2", "currentPlayers": 3, "maxPlayers": 5},
    ]
    mock_sio.emit.assert_awaited_once_with("game_list", expected_game_list, room="games:list")