import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from services.game_services import GameService


@pytest.fixture
def db_mock():
    db = MagicMock()
    db.commit = MagicMock()
    return db


@pytest.fixture
def repo_mock():
    return MagicMock()


@pytest.fixture
def game_service(db_mock, repo_mock):
    svc = GameService(db_mock)
    svc.repo = repo_mock
    return svc


@pytest.mark.asyncio
async def test_finish_turn_success(game_service):
    # NOTE - Mocking the game itself
    db_game = MagicMock()
    db_game.in_game = True
    db_game.current_turn = 0
    game_service.repo.get_by_id.return_value = db_game

    # NOTE - Mock the first player
    player = MagicMock()
    player.turn = 0
    fake_game_ref = MagicMock()
    fake_game_ref.current_turn = 0
    fake_game_ref.players = [MagicMock(), MagicMock()]
    player.game = fake_game_ref

    # NOTE - Replace search_player_by_id by a mock that returns player
    with patch("services.game_services.search_player_by_id", return_value=player):
        new_turn = await game_service.finish_turn(game_id=1, player_id=10)

    # NOTE expected: (0 + 1) % 2 == 1
    assert new_turn == 1
    assert fake_game_ref.current_turn == 1
    game_service._db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_finish_turn_game_not_found(game_service):
    game_service.repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        await game_service.finish_turn(game_id=999, player_id=1)

    assert exc.value.status_code == 404
    assert "Game not found" in str(exc.value.detail)


@pytest.mark.asyncio
async def test_finish_turn_game_not_started(game_service):
    db_game = MagicMock()
    db_game.in_game = False
    game_service.repo.get_by_id.return_value = db_game

    with pytest.raises(HTTPException) as exc:
        await game_service.finish_turn(game_id=1, player_id=1)

    assert exc.value.status_code == 400
    assert "The game has not started yet" in str(exc.value.detail)


@pytest.mark.asyncio
async def test_finish_turn_not_your_turn(game_service):
    # NOTE - We mock the game with the current turn at 0 (first player)
    db_game = MagicMock()
    db_game.in_game = True
    db_game.current_turn = 0
    game_service.repo.get_by_id.return_value = db_game

    # NOTE - Createsa player with turn 1
    player = MagicMock()
    player.turn = 1
    player.game = MagicMock()
    player.game.players = [MagicMock(), MagicMock()]

    # NOTE - Replace search_player_by_id by a mock that returns player
    with patch("services.game_services.search_player_by_id", return_value=player):
        with pytest.raises(HTTPException) as exc:
            # NOTE - Try to finish turn not in our turn
            await game_service.finish_turn(game_id=1, player_id=42)

    assert exc.value.status_code == 403
    assert "It is not your turn" in str(exc.value.detail)
