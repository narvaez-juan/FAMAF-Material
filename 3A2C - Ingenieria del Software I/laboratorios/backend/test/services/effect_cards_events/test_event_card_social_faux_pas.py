import pytest
from models.card_model import Card, CardType
from models.game_cards_model import GameCards, CardLocation
from models.secret_card_model import Secret
from services.effect_cards_events import CardsEventsEffects
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_sfp_effect_triggers_on_receive(db_session, started_game, seed_cards, monkeypatch):
    """Verifica que el efecto de Social Faux Pas se activa al recibirla por Dead Card Folly."""

    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2_id = started_game["player2"].id

    sfp_card = Card(image="27-devious_fauxpas.png", type=CardType.DEV)
    db_session.add(sfp_card)
    db_session.commit()
    db_session.refresh(sfp_card)

    gc_sfp = GameCards(
        game_id=game_id,
        card_id=sfp_card.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(gc_sfp)
    db_session.commit()
    db_session.refresh(gc_sfp)

    dcf_card = Card(image="25-event_deadcardfolly.png", type=CardType.EVT)
    db_session.add(dcf_card)
    db_session.commit()
    db_session.refresh(dcf_card)

    gc_dcf = GameCards(
        game_id=game_id,
        card_id=dcf_card.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(gc_dcf)
    db_session.commit()
    db_session

import pytest
from models.card_model import Card, CardType
from models.game_cards_model import GameCards, CardLocation
from services.effect_cards_events import CardsEventsEffects
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_sfp_effect_skipped_if_no_secrets(db_session, started_game, seed_cards, monkeypatch):
    """Verifica que el efecto de Social Faux Pas se omite si el receptor no tiene secretos."""

    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2_id = started_game["player2"].id

    sfp_card = Card(image="27-devious_fauxpas.png", type=CardType.DEV)
    db_session.add(sfp_card)
    db_session.commit()
    db_session.refresh(sfp_card)

    gc_sfp = GameCards(
        game_id=game_id,
        card_id=sfp_card.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(gc_sfp)
    db_session.commit()
    db_session.refresh(gc_sfp)

    dcf_card = Card(image="25-event_deadcardfolly.png", type=CardType.EVT)
    db_session.add(dcf_card)
    db_session.commit()
    db_session.refresh(dcf_card)

    gc_dcf = GameCards(
        game_id=game_id,
        card_id=dcf_card.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(gc_dcf)
    db_session.commit()
    db_session.refresh(gc_dcf)

    mock_emit = AsyncMock()
    monkeypatch.setattr("services.card_events.emit_sfp_reveal_secret", mock_emit)

    service = CardsEventsEffects(db_session)
    await service.play_dead_card_folly(
        direction="right",
        cards_to_pass=[[creator_id, gc_sfp.id]],
        game_id=game_id,
        id_dead_card_folly=gc_dcf.id
    )

    mock_emit.assert_not_called()
