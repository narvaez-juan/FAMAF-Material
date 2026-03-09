import pytest
from fastapi import status
from datetime import date
from unittest.mock import patch, AsyncMock, ANY

from services.game_services import GameService
from DTOs.game_dto import GameDTO
from models.player_model import Player
from models.game_model import Game
from models.secret_card_model import Secret, TipoSecreto
from models.game_cards_model import GameCards, CardLocation


@pytest.mark.asyncio
async def test_start_game_success(db_session, test_client, create_game_with_players, seed_cards):
    game_id = create_game_with_players["game_id"]
    creator_id = create_game_with_players["creator_id"]

    with patch("services.game_services.emit_initial_secrets", new_callable=AsyncMock) as mock_emit_secrets, \
    patch("services.game_services.emit_draft_piles", new_callable=AsyncMock) as mock_emit_draft:

        
        response = test_client.post(f"/games/{game_id}/start", json={"player_id": creator_id})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert data["game_id"] == game_id

        mock_emit_secrets.assert_called_once_with(game_id, ANY)
        mock_emit_draft.assert_called_once_with(game_id, ANY)

    game = db_session.get(Game, game_id)
    assert game.in_game is True


    draft_cards = db_session.query(GameCards).filter(
        GameCards.game_id == game_id,
        GameCards.location == CardLocation.DRAFT
    ).all()
    assert len(draft_cards) == 3 

    db_session.close()


@pytest.mark.asyncio
async def test_start_game_not_found(test_client):
    response = test_client.post("/games/999/start", json={"player_id": 1})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Game not found"


@pytest.mark.asyncio
async def test_start_game_not_creator(db_session, test_client, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    player2 = create_game_with_players["player2"]

    response = test_client.post(f"/games/{game_id}/start", json={"player_id": player2.id})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "You don't have permission to start the game"

    db_session.close()


@pytest.mark.asyncio
async def test_start_game_not_enough_players(db_session, test_client):
    service = GameService(db_session)

    dto = GameDTO(
        name="Partida Test",
        min_players=2,
        max_players=4,
        player_name="Creador",
        player_birth_date=date(1990, 1, 1),
    )
    game_id, creator_id = await service.create_game(dto)

    response = test_client.post(f"/games/{game_id}/start", json={"player_id": creator_id})
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert response.json()["detail"] == "The minimum number of players is not met"

    db_session.close()


@pytest.mark.asyncio
async def test_start_game_already_started(db_session, test_client, seed_cards, create_game_with_players, started_game):
    game_id = create_game_with_players["game_id"]
    creator_id = create_game_with_players["creator_id"]

    response = test_client.post(f"/games/{game_id}/start", json={"player_id": creator_id})
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert response.json()["detail"] == "The game was started"

    db_session.close()


@pytest.mark.asyncio
async def test_start_game_secrets_five_players(db_session, test_client, seed_cards, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    creator_id = create_game_with_players["creator_id"]

    players = []
    for i in range(3):
        p = Player(
            name=f"Jugador{i+1}",
            birthdate=date(1990, 1, 1),
            game_id=game_id,
            turn=i + 1,
        )
        db_session.add(p)
        players.append(p)
    db_session.commit()

    with patch("services.game_services.emit_initial_secrets", new_callable=AsyncMock) as mock_emit_secrets, \
    patch("services.game_services.emit_draft_piles", new_callable=AsyncMock) as mock_emit_draft:


        response = test_client.post(f"/games/{game_id}/start", json={"player_id": creator_id})
        assert response.status_code == status.HTTP_200_OK

        mock_emit_secrets.assert_called_once_with(game_id, ANY)
        mock_emit_draft.assert_called_once_with(game_id, ANY)

    db_session.expire_all()
    updated_game = db_session.get(Game, game_id)
    assert updated_game.in_game is True

    secrets = db_session.query(Secret).filter(Secret.game_id == game_id).all()
    assert len(secrets) == 5 * 3  

    for p in players:
        player_secrets = [s for s in secrets if s.player_id == p.id]
        assert len(player_secrets) == 3

    types = [s.secret_type for s in secrets]
    assert TipoSecreto.MURDERER in types
    assert TipoSecreto.ACCOMPLICE in types
    assert any(t == TipoSecreto.OTRO for t in types)
    assert all(not s.revealed for s in secrets)

    draft_cards = db_session.query(GameCards).filter(
        GameCards.game_id == game_id,
        GameCards.location == CardLocation.DRAFT
    ).all()
    assert len(draft_cards) == 3


@pytest.mark.asyncio
async def test_start_game_secrets_three_players(db_session, test_client, seed_cards):
    game = Game(
        name="Partida Mockeada 3 Jugadores",
        min_players=2,
        max_players=3,
        players_amount=0,
        in_game=False,
    )
    db_session.add(game)
    db_session.commit()

    players = []
    for i in range(3):
        p = Player(
            name=f"Jugador{i+1}",
            birthdate=date(1990, 1, 1),
            game_id=game.id,
            turn=i + 1,
        )
        db_session.add(p)
        players.append(p)
    db_session.commit()
    creator = players[0]

    with patch("services.game_services.emit_initial_secrets", new_callable=AsyncMock) as mock_emit_secrets, \
    patch("services.game_services.emit_draft_piles", new_callable=AsyncMock) as mock_emit_draft:


        response = test_client.post(f"/games/{game.id}/start", json={"player_id": creator.id})
        assert response.status_code == status.HTTP_200_OK

        mock_emit_secrets.assert_called_once_with(game.id, ANY)
        mock_emit_draft.assert_called_once_with(game.id, ANY)

    db_session.expire_all()
    updated_game = db_session.get(Game, game.id)
    assert updated_game.in_game is True

    secrets = db_session.query(Secret).filter(Secret.game_id == game.id).all()
    assert len(secrets) == 3 * 3

    for p in players:
        player_secrets = [s for s in secrets if s.player_id == p.id]
        assert len(player_secrets) == 3

    types = [s.secret_type for s in secrets]
    assert TipoSecreto.MURDERER in types
    assert TipoSecreto.ACCOMPLICE not in types
    assert any(t == TipoSecreto.OTRO for t in types)
    assert all(not s.revealed for s in secrets)

    draft_cards = db_session.query(GameCards).filter(
        GameCards.game_id == game.id,
        GameCards.location == CardLocation.DRAFT
    ).all()
    assert len(draft_cards) == 3
