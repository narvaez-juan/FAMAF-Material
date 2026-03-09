import pytest

from services.set_services import SetService
from services.exceptions import (
    GameNotFoundError,
    PlayerNotFoundError,
    SetNotFoundError,
    badRequestError,
)

pytestmark = pytest.mark.asyncio


@pytest.fixture(autouse=True)
def mute_emits(monkeypatch):
    """
    Avoids side effects from real-time emissions during tests.
    Patches the helpers imported within the services module.
    """
    import services.set_services as ss

    async def _noop(*args, **kwargs):
        return None

    monkeypatch.setattr(ss, "emit_player_sets", _noop)
    monkeypatch.setattr(ss, "emit_all_sets", _noop)


async def test_steal_set_success_transfers_ownership(
    db_session, create_game_with_players_and_sets
):
    svc = SetService(db_session)
    data = create_game_with_players_and_sets
    game_id = data["game_id"]
    creator_id = data["creator_id"]
    player2_id = data["player2_id"]

    # Select a set owned by player2
    from models.set_model import SetPlay
    sett_before = (
        db_session.query(SetPlay)
        .filter_by(game_id=game_id, owner_id=player2_id)
        .first()
    )
    assert sett_before, "No se encontró un set con owner=player2 en el fixture"
    chosen_set_id = sett_before.id

    assert sett_before.owner_id == player2_id

    await svc.steal_set(game_id=game_id, player_id=creator_id, chosen_set_id=chosen_set_id)

    sett_after = db_session.query(SetPlay).get(chosen_set_id)
    assert sett_after is not None
    assert sett_after.owner_id == creator_id


async def test_steal_set_game_not_found_raises(
    db_session, create_game_with_players_and_sets
):
    svc = SetService(db_session)
    data = create_game_with_players_and_sets
    creator_id = data["creator_id"]
    chosen_set_id = data["sets"][0]["set_id"]

    with pytest.raises(GameNotFoundError):
        await svc.steal_set(
            game_id=999999, player_id=creator_id, chosen_set_id=chosen_set_id
        )


async def test_steal_set_player_not_found_raises(
    db_session, create_game_with_players_and_sets
):
    svc = SetService(db_session)
    data = create_game_with_players_and_sets
    game_id = data["game_id"]
    chosen_set_id = data["sets"][0]["set_id"]

    with pytest.raises(PlayerNotFoundError):
        await svc.steal_set(
            game_id=game_id, player_id=999999, chosen_set_id=chosen_set_id
        )


async def test_steal_set_set_not_found_raises(
    db_session, create_game_with_players_and_sets
):
    svc = SetService(db_session)
    data = create_game_with_players_and_sets
    game_id = data["game_id"]
    creator_id = data["creator_id"]

    with pytest.raises(SetNotFoundError):
        await svc.steal_set(game_id=game_id, player_id=creator_id, chosen_set_id=999999)


async def test_steal_set_cannot_steal_own_set_raises_bad_request(
    db_session, create_game_with_players_and_sets
):
    """
    Must fail if the player tries to steal a set that already belongs to him.
    """
    svc = SetService(db_session)
    data = create_game_with_players_and_sets
    game_id = data["game_id"]
    player2_id = data["player2_id"]

    # Buscar un set que pertenezca a player2 directamente en la BD
    from models.set_model import SetPlay
    set_owned_by_player2 = (
        db_session.query(SetPlay)
        .filter_by(game_id=game_id, owner_id=player2_id)
        .first()
    )
    assert set_owned_by_player2, "No se encontró un set con owner=player2 en el fixture"

    # Tries to 'steal' his own set should raise badRequestError
    from services.exceptions import badRequestError
    with pytest.raises(badRequestError) as exc:
        await svc.steal_set(
            game_id=game_id,
            player_id=player2_id,                # mismo dueño
            chosen_set_id=set_owned_by_player2.id,  # el set ya es suyo
        )

    assert "cannot steal" in str(exc.value).lower()

    # Invariants: the owner did not change
    unchanged = db_session.query(SetPlay).get(set_owned_by_player2.id)
    assert unchanged.owner_id == player2_id
