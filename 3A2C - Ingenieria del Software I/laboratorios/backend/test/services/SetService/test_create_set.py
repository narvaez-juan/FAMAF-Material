import pytest
import pytest_asyncio
from sqlalchemy.orm import Session

from models.card_model import CardType
from models.game_cards_model import GameCards, CardLocation
from models.set_model import SetType, SetState
from services.set_services import SetService


def _mk_card(db: Session, image: str, ctype: CardType = CardType.DET):
    """Crea una Card DET con image deseada y devuelve la instancia."""
    from models import Card

    card = Card(image=image, type=ctype)
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


def _mk_game_card(
    db: Session,
    *,
    game_id: int,
    card_id: int,
    owner_id: int,
    location=CardLocation.HAND
):
    """Asocia Card a una partida/owner en HAND y devuelve GameCards."""
    gc = GameCards(
        game_id=game_id,
        card_id=card_id,
        owner_id=owner_id,
        location=location,
    )
    db.add(gc)
    db.commit()
    db.refresh(gc)
    return gc


async def _build_and_create_set(
    db: Session, game_id: int, owner_id: int, images: list[str]
):
    """Crea cartas DET con las images dadas, las asigna al owner en HAND, y ejecuta create_set."""
    gcs = []
    for img in images:
        c = _mk_card(db, img, CardType.DET)
        gc = _mk_game_card(
            db,
            game_id=game_id,
            card_id=c.id,
            owner_id=owner_id,
            location=CardLocation.HAND,
        )
        gcs.append(gc)

    emitted = {
        "emit_player_sets": [],
        "emit_all_sets": [],
        "emit_player_hand": [],
        "emit_set_effects": [],
    }

    async def fake_emit_player_sets(game_id_, player_id_, db_):
        emitted["emit_player_sets"].append((game_id_, player_id_))

    async def fake_emit_all_sets(game_id_, db_):
        emitted["emit_all_sets"].append(game_id_)

    async def fake_emit_player_hand(game_id_, player_id_, db_):
        emitted["emit_player_hand"].append((game_id_, player_id_))

    async def fake_emit_set_effects(set_play, game_id_, card_ids_):
        emitted["emit_set_effects"].append((set_play, game_id_, list(card_ids_)))

    import services.set_services as ss

    old_eps, old_eas, old_eph, old_ese = (
        ss.emit_player_sets,
        ss.emit_all_sets,
        ss.emit_player_hand,
        ss.emit_set_effects,
    )
    ss.emit_player_sets = fake_emit_player_sets
    ss.emit_all_sets = fake_emit_all_sets
    ss.emit_player_hand = fake_emit_player_hand
    ss.emit_set_effects = fake_emit_set_effects

    try:
        svc = SetService(db)
        new_set = await svc.create_set([gc.id for gc in gcs], owner_id, game_id)
    finally:
        # Restore
        (
            ss.emit_player_sets,
            ss.emit_all_sets,
            ss.emit_player_hand,
            ss.emit_set_effects,
        ) = (old_eps, old_eas, old_eph, old_ese)

    return new_set, gcs, emitted


@pytest.mark.asyncio
async def test_create_set_poirot_ok(db_session, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    owner_id = create_game_with_players["creator_id"]
    # Regla Poirot: 3 cartas DET, al menos una empieza con "07" y las demás "07"/"14"
    new_set, gcs, emitted = await _build_and_create_set(
        db_session,
        game_id,
        owner_id,
        ["07-detective_poirot.png", "14-detective_quin.png", "14-detective_quin.png"],
    )

    assert new_set.set_type == SetType.HERCULE_POIROT
    assert new_set.effect.name == "REVEAL_BY_ACTOR"
    assert new_set.state == SetState.PENDING_SELECTION
    assert new_set.wildcard is True

    # Las cartas quedan asociadas al set y movidas a SET
    for gc in gcs:
        db_session.refresh(gc)
        assert gc.set_id == new_set.id
        assert gc.location == CardLocation.SET

    # Se emiten los 4 eventos del flujo de create_set
    assert emitted["emit_player_sets"] == [(game_id, owner_id)]
    assert emitted["emit_all_sets"] == [game_id]
    assert emitted["emit_player_hand"] == [(game_id, owner_id)]
    # emit_set_effects recibe el set, el game_id y los ids de game_cards
    s, gid, ids = emitted["emit_set_effects"][0]
    assert (
        s.id == new_set.id and gid == game_id and set(ids) == set(gc.id for gc in gcs)
    )


@pytest.mark.asyncio
async def test_create_set_marple_ok(db_session, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    owner_id = create_game_with_players["creator_id"]

    new_set, gcs, _ = await _build_and_create_set(
        db_session,
        game_id,
        owner_id,
        ["08-detective_marple.png", "14-detective_quin.png", "08-detective_marple.png"],
    )
    assert new_set.set_type == SetType.MISS_MARPLE
    assert new_set.effect.name == "REVEAL_BY_ACTOR"
    assert new_set.wildcard is True


@pytest.mark.asyncio
async def test_create_set_satterthwaite_ok(db_session, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    owner_id = create_game_with_players["creator_id"]

    new_set, gcs, _ = await _build_and_create_set(
        db_session,
        game_id,
        owner_id,
        ["09-detective_satterthwaite.png", "09-detective_satterthwaite.png"],
    )
    assert new_set.set_type == SetType.MR_SATTERTHWAITE
    assert new_set.effect.name == "REVEAL_BY_TARGET"
    assert new_set.wildcard is False
    for gc in gcs:
        db_session.refresh(gc)
        assert gc.set_id == new_set.id
        assert gc.location == CardLocation.SET


@pytest.mark.asyncio
async def test_create_set_satterthwaite_with_harley_quinn_ok(db_session, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    owner_id = create_game_with_players["creator_id"]

    new_set, gcs, _ = await _build_and_create_set(
        db_session,
        game_id,
        owner_id,
        ["09-detective_satterthwaite.png", "14-detective_quin.png"],
    )
    assert new_set.set_type == SetType.MR_SATTERTHWAITE
    assert new_set.effect.name == "STEAL"
    assert new_set.wildcard is True
    for gc in gcs:
        db_session.refresh(gc)
        assert gc.set_id == new_set.id
        assert gc.location == CardLocation.SET


@pytest.mark.asyncio
async def test_create_set_parker_pyne_ok(db_session, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    owner_id = create_game_with_players["creator_id"]

    new_set, _, _ = await _build_and_create_set(
        db_session,
        game_id,
        owner_id,
        ["10-detective_pyne.png", "14-detective_quin.png"],
    )
    assert new_set.set_type == SetType.PARKER_PYNE
    assert new_set.effect.name == "HIDE"
    assert new_set.wildcard is True


@pytest.mark.asyncio
async def test_create_set_brent_ok(db_session, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    owner_id = create_game_with_players["creator_id"]

    new_set, _, _ = await _build_and_create_set(
        db_session,
        game_id,
        owner_id,
        ["11-detective_brent.png", "14-detective_quin.png"],
    )
    assert new_set.set_type == SetType.LADY_EILEEN_BUNDLE_BRENT
    assert new_set.effect.name == "REVEAL_BY_TARGET"


@pytest.mark.asyncio
async def test_create_set_tommy_ok(db_session, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    owner_id = create_game_with_players["creator_id"]

    new_set, _, _ = await _build_and_create_set(
        db_session,
        game_id,
        owner_id,
        [
            "12-detective_tommy.png",
            "13-detective_tuppence.png",
        ],  # Tommy acepta 12/13/14
    )
    assert new_set.set_type == SetType.TOMMY_BERESFORD
    assert new_set.effect.name == "REVEAL_BY_TARGET"
    assert new_set.wildcard is False  # no hay 14


@pytest.mark.asyncio
async def test_create_set_tuppence_ok(db_session, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    owner_id = create_game_with_players["creator_id"]

    new_set, _, _ = await _build_and_create_set(
        db_session,
        game_id,
        owner_id,
        ["13-detective_tuppence.png", "14-detective_quin.png"],
    )
    assert new_set.set_type == SetType.TUPPENCE_BERESFORD
    assert new_set.effect.name == "REVEAL_BY_TARGET"
    assert new_set.wildcard is True


@pytest.mark.asyncio
async def test_create_set_error_cantidad_incorrecta(
    db_session, create_game_with_players
):
    game_id = create_game_with_players["game_id"]
    owner_id = create_game_with_players["creator_id"]

    # Poirot requiere 3 cartas, acá solo 2 → set inválido
    with pytest.raises(ValueError, match="do not form a valid set"):
        await _build_and_create_set(
            db_session,
            game_id,
            owner_id,
            ["07-detective_poirot.png", "14-detective_quin.png"],
        )


@pytest.mark.asyncio
async def test_create_set_error_owner_mezclado(db_session, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    owner1 = create_game_with_players["creator_id"]
    owner2 = create_game_with_players["player2"].id

    c1 = _mk_card(db_session, "07-detective_poirot.png", CardType.DET)
    c2 = _mk_card(db_session, "14-detective_quin.png", CardType.DET)
    c3 = _mk_card(db_session, "14-detective_quin.png", CardType.DET)

    gc1 = _mk_game_card(
        db_session,
        game_id=game_id,
        card_id=c1.id,
        owner_id=owner1,
        location=CardLocation.HAND,
    )
    gc2 = _mk_game_card(
        db_session,
        game_id=game_id,
        card_id=c2.id,
        owner_id=owner2,
        location=CardLocation.HAND,
    )  # distinto owner
    gc3 = _mk_game_card(
        db_session,
        game_id=game_id,
        card_id=c3.id,
        owner_id=owner1,
        location=CardLocation.HAND,
    )

    svc = SetService(db_session)
    # GameCardsRepository.get_cards_for_set debería retornar menos que len(card_ids)
    with pytest.raises(ValueError, match="Some cards are invalid or do not belong"):
        await svc.create_set([gc1.id, gc2.id, gc3.id], owner1, game_id)


@pytest.mark.asyncio
async def test_create_set_error_tipo_invalido(db_session, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    owner_id = create_game_with_players["creator_id"]

    # Cartas tipo EVT no deberían calificar
    evt1 = _mk_card(db_session, "07-not_detective.png", CardType.EVT)
    evt2 = _mk_card(db_session, "14-not_detective.png", CardType.EVT)
    evt3 = _mk_card(db_session, "14-not_detective2.png", CardType.EVT)

    gc1 = _mk_game_card(
        db_session,
        game_id=game_id,
        card_id=evt1.id,
        owner_id=owner_id,
        location=CardLocation.HAND,
    )
    gc2 = _mk_game_card(
        db_session,
        game_id=game_id,
        card_id=evt2.id,
        owner_id=owner_id,
        location=CardLocation.HAND,
    )
    gc3 = _mk_game_card(
        db_session,
        game_id=game_id,
        card_id=evt3.id,
        owner_id=owner_id,
        location=CardLocation.HAND,
    )

    svc = SetService(db_session)
    with pytest.raises(ValueError, match="do not form a valid set"):
        await svc.create_set([gc1.id, gc2.id, gc3.id], owner_id, game_id)


@pytest.mark.asyncio
async def test_create_set_error_card_ids_no_corresponden_al_owner(
    db_session, create_game_with_players
):
    game_id = create_game_with_players["game_id"]
    owner1 = create_game_with_players["creator_id"]
    owner2 = create_game_with_players["player2"].id

    # Creamos 2 gcs del owner1 y 1 gc del owner2, pero invocamos con owner1
    c1 = _mk_card(db_session, "10-detective_pyne.png", CardType.DET)
    c2 = _mk_card(db_session, "14-detective_quin.png", CardType.DET)
    gc1 = _mk_game_card(db_session, game_id=game_id, card_id=c1.id, owner_id=owner1)
    gc2 = _mk_game_card(db_session, game_id=game_id, card_id=c2.id, owner_id=owner2)

    svc = SetService(db_session)
    with pytest.raises(ValueError, match="Some cards are invalid or do not belong"):
        await svc.create_set([gc1.id, gc2.id], owner1, game_id)
