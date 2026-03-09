import pytest
from models.secret_card_model import Secret, TipoSecreto
from services.secret_card_service import SecretService
from DTOs.secret_dto import SecretDTO
from unittest.mock import AsyncMock, patch, Mock
from repositories.secret_card_repository import SecretoRepository


@pytest.fixture
def mock_sio_emit():
    with patch("realtime.sockets.sio.emit", new_callable=AsyncMock) as mock_emit:
        yield mock_emit

@pytest.fixture
def service(db_session):
    return SecretService(db_session)


@pytest.fixture
def sample_secret_dto():
    return SecretDTO(
        secret_name="You are the Murderer",
        description="This player is the killer.",
        secret_type=TipoSecreto.MURDERER,
        player_id=1,
        game_id=1,
        revealed=False
    )


def test_create_secret_success(service, sample_secret_dto):
    secret = service.create_secret(sample_secret_dto)
    assert secret.id is not None
    assert secret.secret_name == "You are the Murderer"
    assert secret.revealed is False


def test_group_secrets_by_player(service, db_session):

    s1 = Secret(secret_name="A", description="", secret_type=TipoSecreto.MURDERER, player_id=1, game_id=1)
    s2 = Secret(secret_name="B", description="", secret_type=TipoSecreto.ACCOMPLICE, player_id=1, game_id=1)
    s3 = Secret(secret_name="C", description="", secret_type=TipoSecreto.MURDERER, player_id=2, game_id=1)
    db_session.add_all([s1, s2, s3])
    db_session.commit()

    grouped = service.group_secrets_by_player([s1, s2, s3])

    assert len(grouped) == 2
    assert len(grouped[1]) == 2
    assert len(grouped[2]) == 1
    assert grouped[1][0]["secret_name"] == "A"


@pytest.mark.asyncio
async def test_reveal_and_hide_secret(service, db_session, create_game_with_players_and_secrets):
    game_id = create_game_with_players_and_secrets["game_id"]
    secrets = create_game_with_players_and_secrets["secrets"]
    creator_id = create_game_with_players_and_secrets["creator_id"]
    player2_id = create_game_with_players_and_secrets["player2_id"]

    secret_repo = SecretoRepository(db_session)

    # reveal a hide Secret
    await service.update_secret_state_service(game_id, creator_id, secrets[0]["secret_id"], "REVEAL")
    secret = secret_repo.get_by_id(secrets[0]["secret_id"])
    assert secret.revealed == True

    # hide a revealed Secret
    await service.update_secret_state_service(game_id, player2_id, secrets[3]["secret_id"], "HIDE")
    secret = secret_repo.get_by_id(secrets[3]["secret_id"])
    assert secret.revealed == False


@pytest.mark.asyncio
async def test_reveal_murderer_secret(secret_service, create_game_with_players_and_murderer_secret, db_session):
    data = create_game_with_players_and_murderer_secret
    game_id = data["game_id"]
    creator_id = data["creator_id"]

    murderer_secret = next(s for s in data["secrets"] if s["player_id"] == creator_id and s["secret_type"] == "MURDERER")
    secret_id = murderer_secret["secret_id"]

    await secret_service.update_secret_state_service(game_id, creator_id, secret_id, "REVEAL")

    repo = SecretoRepository(db_session)
    updated = repo.get_by_id(secret_id)
    assert updated is not None
    assert updated.revealed is True


@pytest.mark.asyncio
async def test_verify_into_social_disgrace_calls_emit(db_session, mock_sio_emit,):
    service = SecretService(db_session)

    secret1 = Mock(revealed=True)
    secret2 = Mock(revealed=True)
    service.repo.get_by_player_id = Mock(return_value=[secret1, secret2])

    await service.verify_into_social_disgrace(player_id=1, game_id=1)

    mock_sio_emit.assert_called_once_with(
        "social_disgrace",
        {"player_id": 1, "message": "player has revealed all his secrets."},
        room="game:1"
    )


@pytest.mark.asyncio
async def test_verify_out_social_disgrace_calls_emit(db_session, mock_sio_emit,):
    service = SecretService(db_session)

    secret1 = Mock(revealed=False)
    secret2 = Mock(revealed=True)
    service.repo.get_by_player_id = Mock(return_value=[secret1, secret2])

    await service.verify_out_of_social_disgrace(player_id=1, game_id=1)

    mock_sio_emit.assert_called_once_with(
        "out_social_disgrace",
        {"player_id": 1, "message": "player has hidden at least one of his secrets."},
        room="game:1"
    )