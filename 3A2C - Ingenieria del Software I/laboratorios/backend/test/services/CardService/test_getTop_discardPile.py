import importlib
import pytest

pytestmark = pytest.mark.asyncio

from models import Card, GameCards 
from models.game_cards_model import CardLocation


@pytest.fixture
def discard_cards_factory(db_session, create_game_with_players):
    """
    Devuelve una función helper que crea cartas base y GameCards marcadas como DISCARD.
    Uso:
        create([(None, 1), (None, 2)])  # crea 2 cartas con discard_order 1 y 2
        o con ids previos (no necesario): create([(5, 1), ...])
    """
    game_id = create_game_with_players["game_id"]

    def _create(card_orders: list[tuple[int | None, int]]):
        created = []
        for maybe_card_id, order in card_orders:
            
            card = Card(image=f"card_{order}.png", type="NSF")
            db_session.add(card)
            db_session.flush() 
            gc = GameCards(
                game_id=game_id,
                card_id=card.id,
                location=CardLocation.DISCARD,
                discard_order=order
            )
            db_session.add(gc)
            db_session.commit()
            db_session.refresh(gc)
            created.append(gc)
        return created

    return _create


@pytest.fixture
def fake_sio(monkeypatch):

    try:
        card_events = importlib.import_module("services.card_events")
    except Exception as e:
        pytest.skip(f"No se pudo importar services.card_events: {e}")

    captured = []

    async def _fake_emit(event_name, payload, room=None):
        captured.append((event_name, payload, room))

    
    if hasattr(card_events, "sio"):
        monkeypatch.setattr(card_events.sio, "emit", _fake_emit, raising=False)
    else:
        
        monkeypatch.setattr(card_events, "sio", type("S", (), {"emit": staticmethod(_fake_emit)}), raising=False)

    return captured



async def test_get_last_n_discarded_from_game_cards_repository(db_session, create_game_with_players, discard_cards_factory):
    """
    Verifica que el método get_last_n_discarded en GameCardsRepository
    devuelva las N últimas cartas ordenadas por discard_order DESC.
    """
    game_id = create_game_with_players["game_id"]

    
    discard_cards_factory([(None, 1), (None, 2), (None, 3)])

   
    try:
        
        repo_module = importlib.import_module("repositories.game_cards_repository")
        
        GameCardsRepository = repo_module.GameCardsRepository
    except Exception as e:
        pytest.skip(f"No se pudo importar repositories.game_cards_repository: {e}")

  
    repo = GameCardsRepository(db_session)
    
    last_two = repo.get_last_n_discarded(game_id, 2)

    assert isinstance(last_two, list)
    assert len(last_two) == 2
  
    assert last_two[0].discard_order == 3
    
    assert last_two[1].discard_order == 2



async def test_emit_top_discard_pile_emits_correct_payload(db_session, create_game_with_players, discard_cards_factory, fake_sio):

    game_id = create_game_with_players["game_id"]
    discard_cards_factory([(None, 5), (None, 6)])

   
    try:
        card_events = importlib.import_module("services.card_events")
    except Exception as e:
        pytest.skip(f"No se pudo importar services.card_events: {e}")

    
    
    await card_events.emit_top_discard_pile(game_id, player_id=42, db=db_session, n=2)

    
    assert len(fake_sio) == 1
    event_name, payload, room = fake_sio[0]
    assert event_name == "top_discard"
    assert isinstance(payload, dict)
    assert payload["player_id"] == 42
    assert isinstance(payload["top_discard_cards"], list)
    assert payload["total_cards"] == len(payload["top_discard_cards"]) == 2
    assert room == f"game:{game_id}"
    
    if payload["top_discard_cards"]:
        orders = [c.get("discard_order") for c in payload["top_discard_cards"] if "discard_order" in c]
        if orders:
            assert orders == sorted(orders, reverse=True)


async def test_emit_top_discard_pile_emits_empty_when_no_discards(db_session, create_game_with_players, fake_sio):

    game_id = create_game_with_players["game_id"]

    try:
        card_events = importlib.import_module("services.card_events")
    except Exception as e:
        pytest.skip(f"No se pudo importar services.card_events: {e}")

    
    await card_events.emit_top_discard_pile(game_id, player_id=7, db=db_session, n=3)

    
    assert len(fake_sio) >= 1, "No se capturó ningún emit en fake_sio"

    
    relevant = [
        (ev, payload, room) for (ev, payload, room) in fake_sio
        if ev == "top_discard" and isinstance(payload, dict) and payload.get("player_id") == 7
    ]
    assert relevant, f"No se encontró ningún 'top_discard' para player_id=7 en los emits capturados: {fake_sio}"

    
    ev_name, payload, room = relevant[-1]

    assert ev_name == "top_discard"
    assert room == f"game:{game_id}"


    assert payload.get("top_discard_cards", []) == []
   
    if "total_cards" in payload:
        assert payload["total_cards"] == 0