import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from services.game_services import GameService
from DTOs.player_dto import PlayerDTO
from models.player_model import Player
from models.game_model import Game
from schemas.player_schema import PlayerResponse


@pytest.fixture
def db_mock():
    db = MagicMock()
    db.add = MagicMock()
    db.commit = MagicMock()
    return db


@pytest.fixture
def repo_mock():
    repo = MagicMock()
    return repo


@pytest.fixture
def game_service(db_mock):
    service = GameService(db_mock)
    service.repo = MagicMock()
    return service


@pytest.mark.asyncio
async def test_join_game_success(game_service):
    game = MagicMock(spec=Game)
    game.id = 1
    game.in_game = False
    game.players_amount = 1

    player_dto = PlayerDTO(name="Alice", birthdate="2000-01-01")
    game_service.repo.get_by_id.return_value = game

    # Patch emit_game_list to avoid side effects
    with patch("services.game_events.emit_game_list", new=AsyncMock()):
        # Patch Player to avoid DB side effects
        with patch("services.game_services.Player", autospec=True) as PlayerMock:
            player_instance = PlayerMock.return_value
            player_instance.id = 10
            player_instance.name = "Alice"
            player_instance.birthdate = "2000-01-01"

            result = await game_service.join_game(game_id=1, player=player_dto)

            assert isinstance(result, PlayerResponse)
            assert result.player_id == 10
            assert result.name == "Alice"
            assert result.birthdate == "2000-01-01"
            game_service._db.add.assert_called_once_with(player_instance)
            game_service._db.commit.assert_called_once()
            assert game.players_amount == 2


@pytest.mark.asyncio
async def test_join_game_game_not_found(game_service):
    game_service.repo.get_by_id.return_value = None
    player_dto = PlayerDTO(name="Bob", birthdate="1990-01-01")

    with pytest.raises(Exception) as excinfo:
        await game_service.join_game(game_id=99, player=player_dto)
    assert excinfo.value.status_code == 404
    assert "Game not found" in str(excinfo.value.detail)


@pytest.mark.asyncio
async def test_join_game_game_already_started(game_service):
    game = MagicMock(spec=Game)
    game.id = 2
    game.in_game = True
    game_service.repo.get_by_id.return_value = game
    player_dto = PlayerDTO(name="Carol", birthdate="1985-05-05")

    with pytest.raises(Exception) as excinfo:
        await game_service.join_game(game_id=2, player=player_dto)
    assert excinfo.value.status_code == 400
    assert "Game has already started" in str(excinfo.value.detail)

@pytest.mark.asyncio
async def test_join_game_game_full(game_service):
    game = MagicMock(spec=Game)
    game.id = 3
    game.in_game = False
    game.players_amount = 4
    game.max_players = 4
    game_service.repo.get_by_id.return_value = game
    player_dto = PlayerDTO(name="Dave", birthdate="1995-12-12")

    with pytest.raises(Exception) as excinfo:
        await game_service.join_game(game_id=3, player=player_dto)
    assert excinfo.value.status_code == 400
    assert "Game is full" in str(excinfo.value.detail)