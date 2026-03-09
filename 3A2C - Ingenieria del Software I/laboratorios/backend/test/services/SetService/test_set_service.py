import pytest
from unittest.mock import AsyncMock, Mock, patch
from services.set_services import SetService
from models.set_model import SetType
from services.exceptions import badRequestError, SetNotFoundError


@pytest.fixture
def mock_sio_emit():
    with patch("realtime.sockets.sio.emit", new_callable=AsyncMock) as mock_emit:
        yield mock_emit


@pytest.fixture
def service(db_session):
    service = SetService(db_session)
    service.game_repo.get_by_id = Mock(return_value=Mock(id=1))
    service.player_repo.get_player_by_id = Mock(return_value=Mock(id=1, game_id=1))
    return service


@pytest.mark.asyncio
async def test_play_set_poirot_calls_update_secret_state_service(service):
    service.repo.get_by_id = Mock(return_value=Mock(set_type=SetType.HERCULE_POIROT))
    service.secret_service.update_secret_state_service = AsyncMock()

    result = await service.play_set(1, 1, 1, chosen_secret_id=5)
    assert result["status"] == "ok"

    service.secret_service.update_secret_state_service.assert_awaited_once_with(
        1, 1, 5, "REVEAL"
    )


@pytest.mark.asyncio
async def test_play_set_poirot_missing_secret_raises_bad_request(service):
    service.repo.get_by_id = Mock(return_value=Mock(set_type=SetType.HERCULE_POIROT))

    with pytest.raises(badRequestError, match="chosen_secret_id is required"):
        await service.play_set(1, 1, 1)


@pytest.mark.asyncio
async def test_play_set_parker_pyne_hides_secret(service):
    service.repo.get_by_id = Mock(return_value=Mock(set_type=SetType.PARKER_PYNE))
    service.secret_service.update_secret_state_service = AsyncMock()

    result = await service.play_set(1, 2, 1, chosen_secret_id=99)
    assert result["status"] == "ok"

    service.secret_service.update_secret_state_service.assert_awaited_once_with(
        1, 1, 99, "HIDE"
    )


@pytest.mark.asyncio
async def test_play_set_ariadne_adds_detective_and_emits_event(service, mock_sio_emit):
    ariadne_card = Mock(card=Mock(image="15-detective_oliver.png"), id=55)
    set_mock = Mock(
        set_type=SetType.ARIADNE_OLIVER,
        cards=[ariadne_card],
        owner_id=1,
    )

    service.repo.get_by_id = Mock(return_value=set_mock)
    service.repo.add_detective = Mock()

    result = await service.play_set(
        game_id=1,
        set_id=1,
        target_player_id=1,
        chosen_set_id=10,
    )

    assert result["status"] == "pending_selection"
    service.repo.add_detective.assert_called_once_with(1, 10, 55)
    mock_sio_emit.assert_awaited()
    assert mock_sio_emit.await_count == 4


@pytest.mark.asyncio
async def test_play_set_missing_ariadne_card_raises(service):
    set_mock = Mock(set_type=SetType.ARIADNE_OLIVER, cards=[], owner_id=1)
    service.repo.get_by_id = Mock(return_value=set_mock)

    with pytest.raises(badRequestError, match="Ariadne card not present"):
        await service.play_set(1, 1, 1, chosen_set_id=10)


@pytest.mark.asyncio
async def test_play_set_not_found_raises(service):
    service.repo.get_by_id = Mock(return_value=None)

    with pytest.raises(SetNotFoundError):
        await service.play_set(1, 1, 1)
