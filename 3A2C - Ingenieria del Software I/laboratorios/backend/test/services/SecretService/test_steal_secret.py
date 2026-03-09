# tests/test_secret_service.py
import pytest
from repositories.secret_card_repository import SecretoRepository
from services.secret_card_service import SecretService
from services.exceptions import SecretNotFoundError

pytestmark = pytest.mark.asyncio


async def test_steal_secret(secret_service, create_game_with_players_and_secrets, db_session):

    data = create_game_with_players_and_secrets
    game_id = data["game_id"]
    creator_id = data["creator_id"]
    player2_id = data["player2_id"]
    # buscar un secreto que pertenezca a player2
    secret_entry = next(s for s in data["secrets"] if s["player_id"] == player2_id)
    secret_id = secret_entry["secret_id"]

    # Ejecutar steal
    updated = await secret_service.steal_secret_service(game_id, creator_id, player2_id, secret_id)

    # Verificar que el retorno y la DB reflejan el nuevo owner
    assert updated is not None
    assert getattr(updated, "player_id", None) == creator_id

    repo = SecretoRepository(db_session)
    secret_in_db = repo.get_by_id(secret_id)
    assert secret_in_db is not None
    assert secret_in_db.player_id == creator_id


async def test_update_secret_state_reveal_and_hide(secret_service, create_game_with_players_and_secrets, db_session):

    data = create_game_with_players_and_secrets
    game_id = data["game_id"]
    creator_id = data["creator_id"]
    # seleccionar un secreto del creator (inicialmente revealed = False en el fixture)
    secret_entry = next(s for s in data["secrets"] if s["player_id"] == creator_id)
    secret_id = secret_entry["secret_id"]

    # Reveal
    await secret_service.update_secret_state_service(game_id, creator_id, secret_id, "REVEAL")
    repo = SecretoRepository(db_session)
    secret_after_reveal = repo.get_by_id(secret_id)
    assert secret_after_reveal is not None
    assert secret_after_reveal.revealed is True

    # Hide
    await secret_service.update_secret_state_service(game_id, creator_id, secret_id, "HIDE")
    secret_after_hide = repo.get_by_id(secret_id)
    assert secret_after_hide is not None
    assert secret_after_hide.revealed is False


async def test_update_secret_state_secret_not_found_raises(secret_service, create_game_with_players_and_secrets):

    data = create_game_with_players_and_secrets
    game_id = data["game_id"]
    creator_id = data["creator_id"]
    missing_secret_id = 999999  # ID que no existe en la DB de test

    with pytest.raises(SecretNotFoundError):
        await secret_service.update_secret_state_service(game_id, creator_id, missing_secret_id, "REVEAL")
