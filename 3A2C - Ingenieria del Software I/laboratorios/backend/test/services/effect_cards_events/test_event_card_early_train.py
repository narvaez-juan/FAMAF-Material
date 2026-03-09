import pytest
from models.card_model import Card, CardType
from models.game_cards_model import GameCards, CardLocation
from repositories.game_cards_repository import GameCardsRepository
from services.effect_cards_events import CardsEventsEffects

@pytest.mark.asyncio
async def test_play_early_train_success(db_session, started_game, seed_cards):
    """Test successful execution of Early Train to Paddington."""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]

    event_card = Card(image="24-event_earlytrain.png", type=CardType.EVT)
    db_session.add(event_card)
    db_session.commit()
    db_session.refresh(event_card)

    gc = GameCards(
        game_id=game_id,
        card_id=event_card.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(gc)
    db_session.commit()
    db_session.refresh(gc)

    for i in range(6):
        c = Card(image=f"deck_card_{i}.png", type=CardType.NSF)
        db_session.add(c)
        db_session.flush()
        deck_card = GameCards(
            game_id=game_id,
            card_id=c.id,
            location=CardLocation.DECK,
            position=i + 1
        )
        db_session.add(deck_card)
    db_session.commit()

    service = CardsEventsEffects(db_session)
    await service.play_early_train_to_paddington(
        game_id=game_id,
        player_id=creator_id,
        event_card_id=gc.id
    )

    discarded = db_session.query(GameCards).filter(
        GameCards.game_id == game_id,
        GameCards.location == CardLocation.DISCARD
    ).all()
    assert len(discarded) == 6

    updated_gc = db_session.query(GameCards).filter(GameCards.id == gc.id).first()
    assert updated_gc.location == CardLocation.REMOVED
    assert updated_gc.owner_id is None

@pytest.mark.asyncio
async def test_play_early_train_card_not_found(db_session, started_game):
    """Fails if the event card does not exist."""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]

    service = CardsEventsEffects(db_session)
    with pytest.raises(Exception) as excinfo:
        await service.play_early_train_to_paddington(
            game_id=game_id,
            player_id=creator_id,
            event_card_id=99999
        )
    assert "card" in str(excinfo.value).lower()

@pytest.mark.asyncio
async def test_play_early_train_card_not_owned(db_session, started_game, seed_cards):
    """Fails if the card is not owned by the player."""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]
    player2_id = started_game["player2"].id

    event_card = Card(image="24-event_earlytrain.png", type=CardType.EVT)
    db_session.add(event_card)
    db_session.commit()
    db_session.refresh(event_card)

    gc = GameCards(
        game_id=game_id,
        card_id=event_card.id,
        owner_id=player2_id,
        location=CardLocation.HAND
    )
    db_session.add(gc)
    db_session.commit()
    db_session.refresh(gc)

    service = CardsEventsEffects(db_session)
    with pytest.raises(Exception) as excinfo:
        await service.play_early_train_to_paddington(
            game_id=game_id,
            player_id=creator_id,
            event_card_id=gc.id
        )
    assert "not yours" in str(excinfo.value).lower()

@pytest.mark.asyncio
async def test_play_early_train_with_less_than_six_cards(db_session, started_game, seed_cards):
    """Debe descartar solo las cartas disponibles si hay menos de seis en el mazo."""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]

    event_card = Card(image="24-event_earlytrain.png", type=CardType.EVT)
    db_session.add(event_card)
    db_session.commit()
    db_session.refresh(event_card)

    gc = GameCards(
        game_id=game_id,
        card_id=event_card.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(gc)

    # Solo 3 cartas en el mazo
    db_session.query(GameCards).filter(GameCards.location == CardLocation.DECK).delete()
    db_session.commit()
    
    for i in range(3):
        c = Card(image=f"deck_card_{i}.png", type=CardType.NSF)
        db_session.add(c)
        db_session.flush()
        deck_card = GameCards(
            game_id=game_id,
            card_id=c.id,
            location=CardLocation.DECK,
            position=i + 1
        )
        db_session.add(deck_card)

    db_session.commit()

    service = CardsEventsEffects(db_session)
    await service.play_early_train_to_paddington(
        game_id=game_id,
        player_id=creator_id,
        event_card_id=gc.id
    )

    discarded = db_session.query(GameCards).filter(
        GameCards.game_id == game_id,
        GameCards.location == CardLocation.DISCARD
    ).all()
    assert len(discarded) == 3

@pytest.mark.asyncio
async def test_play_early_train_updates_discard_order(db_session, started_game, seed_cards):
    """Verifica que las cartas descartadas tengan orden incremental."""
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]

    event_card = Card(image="24-event_earlytrain.png", type=CardType.EVT)
    db_session.add(event_card)
    db_session.commit()
    db_session.refresh(event_card)

    gc = GameCards(
        game_id=game_id,
        card_id=event_card.id,
        owner_id=creator_id,
        location=CardLocation.HAND
    )
    db_session.add(gc)

    db_session.query(GameCards).filter(GameCards.location == CardLocation.DECK).delete()
    db_session.commit()
    for i in range(4):
        c = Card(image=f"deck_card_{i}.png", type=CardType.NSF)
        db_session.add(c)
        db_session.flush()
        deck_card = GameCards(
            game_id=game_id,
            card_id=c.id,
            location=CardLocation.DECK,
            position=i + 1
        )
        db_session.add(deck_card)

    db_session.commit()

    service = CardsEventsEffects(db_session)
    await service.play_early_train_to_paddington(
        game_id=game_id,
        player_id=creator_id,
        event_card_id=gc.id
    )

    discarded = db_session.query(GameCards).filter(
        GameCards.game_id == game_id,
        GameCards.location == CardLocation.DISCARD
    ).order_by(GameCards.discard_order).all()

    assert len(discarded) == 4
    assert [c.discard_order for c in discarded] == list(range(1, 5))