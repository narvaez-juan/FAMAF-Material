import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock, AsyncMock, call

from services.effect_cards_events import CardsEventsEffects
from models.game_cards_model import CardLocation, GameCards
from models.card_model import CardType

def test_check_game_not_found(db_session):
    effects = CardsEventsEffects(db_session)

    effects.repo_game.get_by_id = MagicMock(return_value=None)

    with pytest.raises(HTTPException) as excinfo:
        effects.check_game(1)
    assert excinfo.value.status_code == 404
    assert "Game or target player not found" in excinfo.value.detail


def test_check_player_not_found(db_session):
    effects = CardsEventsEffects(db_session)
    effects.repo_player.get_player_by_id = MagicMock(return_value=None)

    with pytest.raises(HTTPException) as excinfo:
        effects.check_player(99)
    assert excinfo.value.status_code == 404
    assert "Game or target player not found" in excinfo.value.detail


def test_check_card_not_found(db_session):
    effects = CardsEventsEffects(db_session)
    effects.repo_game_cards.get_by_id = MagicMock(return_value=None)

    with pytest.raises(HTTPException) as excinfo:
        effects.check_card(10, 1)
    assert excinfo.value.status_code == 404
    assert "Card not found" in excinfo.value.detail


def test_check_card_not_owned(db_session):
    effects = CardsEventsEffects(db_session)

    fake_card = MagicMock()
    fake_card.owner_id = 2
    effects.repo_game_cards.get_by_id = MagicMock(return_value=fake_card)

    with pytest.raises(HTTPException) as excinfo:
        effects.check_card(10, 1)
    assert excinfo.value.status_code == 401
    assert "The card is not yours" in excinfo.value.detail


def test_check_card_valid(db_session):
    effects = CardsEventsEffects(db_session)

    fake_card = MagicMock()
    fake_card.owner_id = 1
    fake_card.card.type = CardType.EVT
    effects.repo_game_cards.get_by_id = MagicMock(return_value=fake_card)

    effects.check_card(10, 1)


def test_change_card_location_discards_specific_card(db_session):
    effects = CardsEventsEffects(db_session)
    db_session.commit = MagicMock()

    fake_card1 = MagicMock()
    fake_card1.id = 10
    fake_card1.card.image = "16-Instant_notsofast.png"
    fake_card1.location = CardLocation.HAND

    fake_card3 = MagicMock()
    fake_card3.id = 5
    fake_card3.card.image = "other.png"
    fake_card3.location = CardLocation.HAND

    effects.change_card_location([fake_card1,fake_card3],10)

    assert fake_card1.location == CardLocation.DISCARD
    assert fake_card3.location == CardLocation.HAND

    db_session.commit.assert_called_once()



@pytest.mark.asyncio
async def test_play_cards_off_the_table_success(db_session):
    effects = CardsEventsEffects(db_session)

    effects.check_card = MagicMock()
    effects.check_player = MagicMock()
    effects.check_game = MagicMock()

    fake_hand = [MagicMock()]
    effects.repo_game_cards.get_hand_player = MagicMock(return_value=fake_hand)
    effects.repo_game_cards.get_card_by_id = MagicMock()
    effects.change_card_location = MagicMock()
    effects._db = MagicMock()

    fake_player = MagicMock()
    fake_player.game_id = 5
    effects.repo_player.get_player_by_id = MagicMock(return_value=fake_player)


    await effects.play_cards_off_the_table(
        player_id=1,
        id_card=10,
        target_player_id=2,
        game_id=5,
    )

    effects.check_card.assert_called_once_with(10, 1)
    
    effects.check_player.assert_has_calls([call(1), call(2)], any_order=True)

    assert effects.check_player.call_count == 2
 

    effects.check_game.assert_called_once_with(5)
    effects.change_card_location.assert_called_once_with(fake_hand, 5)


def test_get_participants_returns_only_involved_players(db_session):
    effects = CardsEventsEffects(db_session)

    fake_players = [MagicMock(id=1), MagicMock(id=2), MagicMock(id=3)]
    effects.repo_game.get_players = MagicMock(return_value=fake_players)

    cards_to_pass = [[1, 101], [3, 103]]  # solo 1 y 3 participan
    participants = effects.get_participants(1, cards_to_pass)

    effects.repo_game.get_players.assert_called_once_with(1)
    assert participants == [1, 3]

def test_calculate_destination_right(db_session):
    effects = CardsEventsEffects(db_session)

    participants = [1, 2, 3]
    cards_to_pass = [[1, 101], [2, 102], [3, 103]]

    result = effects.calculate_destination_of_the_card(participants, cards_to_pass, "right")

    expected = {
        101: 2, 
        102: 3,
        103: 1,
    }

    assert result == expected


def test_calculate_destination_left(db_session):
    effects = CardsEventsEffects(db_session)

    participants = [1, 2, 3]
    cards_to_pass = [[1, 101], [2, 102], [3, 103]]

    result = effects.calculate_destination_of_the_card(participants, cards_to_pass, "left")

    expected = {
        101: 3,  
        102: 1,
        103: 2,
    }

    assert result == expected

@pytest.mark.asyncio
async def test_play_dead_card_folly_success(monkeypatch, db_session):
    effects = CardsEventsEffects(db_session)

    # Mockear métodos internos
    effects.check_game = MagicMock()
    effects.check_direction = MagicMock()
    effects.check_player = MagicMock()
    effects.check_card = MagicMock()
    effects.check_player_to_game = MagicMock()
    effects.get_participants = MagicMock(return_value=[1, 2, 3])
    effects.calculate_destination_of_the_card = MagicMock(return_value={101: 2, 102: 3, 103: 1})
    effects.repo_game_cards.get_card_by_id = MagicMock(side_effect=lambda cid: MagicMock(id=cid))
    effects._db.commit = MagicMock()


    # Mockear eventos async
    mock_emit_dead_card_folly_event = AsyncMock()
    mock_emit_player_hand = AsyncMock()

    monkeypatch.setattr("services.effect_cards_events.emit_dead_card_folly_event", mock_emit_dead_card_folly_event)
    monkeypatch.setattr("services.effect_cards_events.emit_player_hand", mock_emit_player_hand)

    cards_to_pass = [[1, 101], [2, 102], [3, 103]]

    # Carta muerta simulada
    dead_card = MagicMock(id=999)
    effects.repo_game_cards.get_card_by_id = MagicMock(
        side_effect=lambda cid: dead_card if cid == 999 else MagicMock(id=cid)
    )

    await effects.play_dead_card_folly("right", cards_to_pass, 55,id_dead_card_folly=999)

    effects.check_game.assert_called_once_with(55)
    effects.check_direction.assert_called_once_with("right")
    effects.check_player.assert_any_call(1)
    effects.check_card.assert_any_call(101, 1)
    effects._db.commit.assert_called_once()
    assert dead_card.location == CardLocation.DISCARD
    mock_emit_dead_card_folly_event.assert_awaited_once()
    mock_emit_player_hand.assert_awaited()  

@pytest.mark.asyncio
async def test_play_dead_card_folly_returns_if_not_enough_participants(monkeypatch, db_session):
    effects = CardsEventsEffects(db_session)

    effects.check_game = MagicMock()
    effects.check_direction = MagicMock()
    effects.check_player_to_game = MagicMock()
    effects.check_player = MagicMock()
    effects.check_card = MagicMock()
    effects.check_player_to_game = MagicMock()
    effects.get_participants = MagicMock(return_value=[1])

    dead_card = MagicMock(id=999)
    effects.repo_game_cards.get_card_by_id = MagicMock(
        side_effect=lambda cid: dead_card if cid == 999 else MagicMock(id=cid)
    )

    mock_emit_dead_card_folly_event = AsyncMock()
    monkeypatch.setattr("services.effect_cards_events.emit_dead_card_folly_event", mock_emit_dead_card_folly_event)

    result = await effects.play_dead_card_folly("right", [[1, 101]], 55, id_dead_card_folly=999)

    assert result is None  
    mock_emit_dead_card_folly_event.assert_awaited_once()


@pytest.fixture
def setup_service(monkeypatch, db_session):
    """Fixture base para configurar el servicio y los mocks."""
    service = CardsEventsEffects(db_session)

    service.check_card = MagicMock()
    service.check_game = MagicMock()
    service.check_player_to_game = MagicMock()

    service.repo_game_cards = MagicMock()
    service.repo_card_service = MagicMock()
    service._db.commit = MagicMock()

    emit_delay = AsyncMock()
    emit_discard = AsyncMock()
    emit_deck = AsyncMock()
    emit_hand = AsyncMock()

    monkeypatch.setattr("services.effect_cards_events.emit_delay_the_murderer_escape", emit_delay)
    monkeypatch.setattr("services.effect_cards_events.emit_discard_pile", emit_discard)
    monkeypatch.setattr("services.effect_cards_events.emit_deck_size", emit_deck)
    monkeypatch.setattr("services.effect_cards_events.emit_player_hand", emit_hand)


    return {
        "service": service,
        "emit_delay": emit_delay,
        "emit_discard": emit_discard,
        "emit_deck": emit_deck,
        "emit_hand": emit_hand,
    }

@pytest.mark.asyncio
async def test_play_delay_the_murderer_escape_success(setup_service, db_session):
    ctx = setup_service
    service = ctx["service"]

    game_id = 1
    player_id = 10
    id_delay_card = 99
    cards_selected = [1, 2]

    deck_cards = [MagicMock(position=1), MagicMock(position=2)]
    selected_cards = [
        MagicMock(id=1, location=CardLocation.DISCARD),
        MagicMock(id=2, location=CardLocation.DISCARD),
    ]
    delay_card = MagicMock(id=id_delay_card, location=CardLocation.HAND)
    discard_pile = [MagicMock(discard_order=1), MagicMock(discard_order=2)]

    service.repo_game_cards.get_deck.return_value = deck_cards
    service.repo_game_cards.get_card_by_id.side_effect = (
        lambda cid: delay_card if cid == id_delay_card else next((c for c in selected_cards if c.id == cid), None)
    )
    service.repo_game_cards.get_discard_deck.return_value = discard_pile
    service.repo_card_service.get_next_discard_order.return_value = 5

    await service.play_delay_the_murderer_escape(game_id, id_delay_card, player_id, cards_selected)

    for c in deck_cards:
        assert c.position in [3, 4]

    for c in selected_cards:
        assert c.location == CardLocation.DECK
        assert c.owner_id is None
        assert c.position in [1, 2]

    assert delay_card.location == CardLocation.REMOVED
    assert delay_card.discard_order == None

    assert service._db.commit.call_count == 2

    ctx["emit_delay"].assert_awaited_once_with(game_id, player_id)
    ctx["emit_discard"].assert_awaited_once_with(game_id, db_session)
    ctx["emit_deck"].assert_awaited_once_with(game_id, db_session)
    ctx["emit_hand"].assert_awaited_once_with(game_id, player_id, db_session)


@pytest.mark.asyncio
async def test_play_delay_the_murderer_escape_card_not_found(setup_service):
    ctx = setup_service
    service = ctx["service"]

    service.repo_game_cards.get_card_by_id.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        await service.play_delay_the_murderer_escape(
            game_id=1,
            id_delay_the_murderer_escape=999,
            player_id=10,
            cards_selected=[1, 2],
        )

    assert excinfo.value.status_code == 404
    assert "Card" in excinfo.value.detail


@pytest.mark.asyncio
async def test_play_delay_the_murderer_escape_delay_not_in_hand(setup_service):
    ctx = setup_service
    service = ctx["service"]

    delay_card = MagicMock(id=99, location=CardLocation.DECK)
    service.repo_game_cards.get_card_by_id.return_value = delay_card

    with pytest.raises(HTTPException) as excinfo:
        await service.play_delay_the_murderer_escape(
            game_id=1,
            id_delay_the_murderer_escape=99,
            player_id=10,
            cards_selected=[1, 2],
        )

    assert excinfo.value.status_code == 400



@pytest.mark.asyncio
async def test_play_delay_the_murderer_escape_empty_deck_and_discard(setup_service, db_session):
    ctx = setup_service
    service = ctx["service"]

    game_id = 1
    player_id = 10
    id_delay_card = 99

    deck_cards = []  # vacío
    selected_cards = [
        MagicMock(id=1, location=CardLocation.DISCARD),
        MagicMock(id=2, location=CardLocation.DISCARD),
    ]
    delay_card = MagicMock(id=id_delay_card, location=CardLocation.HAND)
    discard_pile = []  # vacío

    service.repo_game_cards.get_deck.return_value = deck_cards
    service.repo_game_cards.get_discard_deck.return_value = discard_pile
    service.repo_game_cards.get_card_by_id.side_effect = (
        lambda cid: delay_card if cid == id_delay_card else next((c for c in selected_cards if c.id == cid), None)
    )
    service.repo_card_service.get_next_discard_order.return_value = 1  # primer descarte

    await service.play_delay_the_murderer_escape(
        game_id, id_delay_card, player_id, [1, 2]
    )

    for c in selected_cards:
        assert c.position in [1, 2]
        assert c.location == CardLocation.DECK

    assert delay_card.location == CardLocation.REMOVED
    assert delay_card.discard_order == None

    ctx["emit_delay"].assert_awaited_once()
    ctx["emit_discard"].assert_awaited_once()

@pytest.mark.asyncio
async def test_play_point_your_suspicion_success(monkeypatch, db_session):
    effects = CardsEventsEffects(db_session)

    effects.check_card = MagicMock()
    effects.check_game = MagicMock()
    effects.check_player_to_game = MagicMock()

    mock_emit_point_your_suspision = AsyncMock()
    mock_emit_player_hand = AsyncMock()
    mock_emit_discard_pile = AsyncMock()
    mock_point_your_suspicion_effect = AsyncMock()
    mock_get_next_discard_order = MagicMock(return_value=5)

    monkeypatch.setattr("services.effect_cards_events.emit_point_your_suspision", mock_emit_point_your_suspision)
    monkeypatch.setattr("services.effect_cards_events.emit_player_hand", mock_emit_player_hand)
    monkeypatch.setattr("services.effect_cards_events.emit_discard_pile", mock_emit_discard_pile)
    monkeypatch.setattr("services.effect_cards_events.point_your_suspicion_effect", mock_point_your_suspicion_effect)
    monkeypatch.setattr("services.effect_cards_events.get_next_discard_order", mock_get_next_discard_order)

    fake_card = MagicMock()
    fake_card.owner_id = 10
    fake_card.location = CardLocation.HAND
    effects.repo_game_cards.get_card_by_id = MagicMock(return_value=fake_card)
    effects._db.commit = MagicMock()

    game_id = 1
    player_id = 10
    event_card_id = 55
    selected_players = [2, 3, 2, 4, 3, 2] 

    await effects.play_point_your_suspisicion(game_id, player_id, selected_players, event_card_id)

    effects.check_card.assert_called_once_with(event_card_id, player_id)
    effects.check_game.assert_called_once_with(game_id)
    effects.check_player_to_game.assert_any_call(player_id, game_id)

    for sp in selected_players:
        effects.check_player_to_game.assert_any_call(sp, game_id)

    mock_emit_point_your_suspision.assert_awaited_once_with(game_id, player_id)
    mock_get_next_discard_order.assert_called_once_with(db_session, game_id)

    assert fake_card.location == CardLocation.DISCARD
    assert fake_card.owner_id is None
    assert fake_card.discard_order == 5
    effects._db.commit.assert_called_once()

    mock_emit_player_hand.assert_awaited_once_with(game_id, 10, db_session)
    mock_emit_discard_pile.assert_awaited_once_with(game_id, db_session)

    mock_point_your_suspicion_effect.assert_awaited_once_with(game_id, 2, 10)


@pytest.mark.asyncio
async def test_play_point_your_suspicion_tie_selects_random(monkeypatch, db_session):
    effects = CardsEventsEffects(db_session)

    effects.check_card = MagicMock()
    effects.check_game = MagicMock()
    effects.check_player_to_game = MagicMock()

    mock_emit_point_your_suspision = AsyncMock()
    mock_emit_player_hand = AsyncMock()
    mock_emit_discard_pile = AsyncMock()
    mock_point_your_suspicion_effect = AsyncMock()
    mock_get_next_discard_order = MagicMock(return_value=1)
    monkeypatch.setattr("services.effect_cards_events.emit_point_your_suspision", mock_emit_point_your_suspision)
    monkeypatch.setattr("services.effect_cards_events.emit_player_hand", mock_emit_player_hand)
    monkeypatch.setattr("services.effect_cards_events.emit_discard_pile", mock_emit_discard_pile)
    monkeypatch.setattr("services.effect_cards_events.point_your_suspicion_effect", mock_point_your_suspicion_effect)
    monkeypatch.setattr("services.effect_cards_events.get_next_discard_order", mock_get_next_discard_order)

    fake_card = MagicMock()
    fake_card.owner_id = 5
    effects.repo_game_cards.get_card_by_id = MagicMock(return_value=fake_card)
    effects._db.commit = MagicMock()

    game_id = 1
    player_id = 5
    event_card_id = 88
    selected_players = [2, 3, 2, 3] 

    monkeypatch.setattr("random.choice", lambda x: 3)

    await effects.play_point_your_suspisicion(game_id, player_id, selected_players, event_card_id)

    mock_point_your_suspicion_effect.assert_awaited_once_with(game_id, 3, 5)


@pytest.mark.asyncio
async def test_play_point_your_suspicion_card_not_found(monkeypatch, db_session):
    effects = CardsEventsEffects(db_session)

    effects.check_card = MagicMock()
    effects.check_game = MagicMock()
    effects.check_player_to_game = MagicMock()
    effects.repo_game_cards.get_card_by_id = MagicMock(return_value=None)

    monkeypatch.setattr("services.effect_cards_events.emit_point_your_suspision", AsyncMock())

    with pytest.raises(AttributeError):
        await effects.play_point_your_suspisicion(
            game_id=1,
            player_id=2,
            selected_players=[3, 4],
            event_card_id=99
        )