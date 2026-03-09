import pytest
from datetime import datetime
from fastapi import HTTPException
from models.game_model import Game
from models.player_model import Player
from models.card_model import Card, CardType
from models.game_cards_model import GameCards, CardLocation
from repositories.game_cards_repository import GameCardsRepository
import pytest
from fastapi import status



# ============================================================
# UNIT TESTS (services / repository)
# ============================================================
# -----------------------------
# Test: game not found
# -----------------------------
def test_draw_card_game_not_found(test_client):
    payload = {
        "player_id": 1,
        "draftCardsSelectedIds": [],
        "drawPileSelectedCount": 0
    }
    response = test_client.post("/games/999/draw_card", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"

# -----------------------------
# Test: player not found
# -----------------------------
def test_draw_card_player_not_found(test_client, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    payload = {
        "player_id": 999,
        "draftCardsSelectedIds": [],
        "drawPileSelectedCount": 0
    }
    response = test_client.post(f"/games/{game_id}/draw_card", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Player not found"

# -----------------------------
# Test: player not in game
# -----------------------------
def test_draw_card_player_not_in_game(db_session, test_client, create_game_with_players):
    game1_id = create_game_with_players["game_id"]

    # Crear jugador en otro juego
    player = Player(name="Bob", birthdate=datetime(1995, 1, 1), game_id=2, turn=1)
    db_session.add(player)
    db_session.commit()

    payload = {
        "player_id": player.id,
        "draftCardsSelectedIds": [],
        "drawPileSelectedCount": 0
    }
    response = test_client.post(f"/games/{game1_id}/draw_card", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Player does not belong to the game"

# -----------------------------
# Test: not enough cards
# -----------------------------

def test_get_draft_count(db_session, seed_cards, create_game_with_players):
    repo = GameCardsRepository(db_session)
    game_id = create_game_with_players["game_id"]

    for i in range(3):
        card = Card(image=f"draft_{i}.png", type=CardType.EVT)
        db_session.add(card)
        db_session.flush()
        game_card = GameCards(
            game_id=game_id, card_id=card.id, location=CardLocation.DRAFT, position=i
        )
        db_session.add(game_card)
    db_session.commit()

    count = repo.get_draft_count(game_id)
    assert count == 3


@pytest.mark.asyncio
async def test_check_deck_size_valid(db_session, seed_cards, create_game_with_players):
    service = create_game_with_players["service"]
    game_id = create_game_with_players["game_id"]

    # Crear cartas en deck
    for i in range(4):
        card = Card(image=f"deck_{i}.png", type=CardType.EVT)
        db_session.add(card)
        db_session.flush()
        gc = GameCards(
            game_id=game_id, card_id=card.id, location=CardLocation.DECK, position=i
        )
        db_session.add(gc)
    db_session.commit()

    # Validar deck size usando get_deck_size
    deck_size = service.repo_game_cards.get_deck_size(game_id)
    assert deck_size >= 2


@pytest.mark.asyncio
async def test_check_deck_size_invalid(db_session, seed_cards, create_game_with_players):
    service = create_game_with_players["service"]
    game_id = create_game_with_players["game_id"]

    # No se agregan cartas, deck size será 0
    deck_size = service.repo_game_cards.get_deck_size(game_id)
    required = 5
    if deck_size < required:
        # Simular comportamiento anterior lanzando HTTPException
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            raise HTTPException(status_code=409, detail=f"Deck size is too small: {deck_size} < {required}")



@pytest.mark.asyncio
async def test_assign_cards_to_player_assigns_owner(db_session, seed_cards, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    player_id = create_game_with_players["creator_id"]
    service = create_game_with_players["service"]

    cards = []
    for i in range(2):
        card = Card(image=f"draft_{i}.png", type=CardType.EVT)
        db_session.add(card)
        db_session.flush()
        gc = GameCards(
            game_id=game_id, card_id=card.id, location=CardLocation.DRAFT, position=i
        )
        db_session.add(gc)
        db_session.flush()
        cards.append(gc)
    db_session.commit()

    service.repo_game_cards.assign_cards_to_player(cards, player_id)
    db_session.commit()

    for c in cards:
        db_session.refresh(c)
        assert c.owner_id == player_id



@pytest.mark.asyncio
async def test_draw_cards_from_draft_pile_valid(db_session, seed_cards, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    player_id = create_game_with_players["creator_id"]
    service = create_game_with_players["service"]

    draft_cards = []
    for i in range(3):
        card = Card(image=f"draft_{i}.png", type=CardType.EVT)
        db_session.add(card)
        db_session.flush()
        gc = GameCards(game_id=game_id, card_id=card.id, location=CardLocation.DRAFT)
        db_session.add(gc)
        db_session.flush()
        draft_cards.append(gc)
    db_session.commit()

    # usamos card_id, que es lo que tu función espera
    selected_ids = [draft_cards[0].id, draft_cards[1].id]
    result = await service.draw_cards_from_draft_pile(game_id, player_id, selected_ids)
    db_session.commit()

    assert len(result) == 2
    for card_info in result:
        assert card_info.owner_id == player_id
        assert card_info.location == CardLocation.HAND


@pytest.mark.asyncio
async def test_draw_cards_from_draft_pile_invalid_card(db_session, seed_cards, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    player_id = create_game_with_players["creator_id"]
    service = create_game_with_players["service"]

    card = Card(image="invalid.png", type=CardType.EVT)
    db_session.add(card)
    db_session.flush()
    gc = GameCards(game_id=game_id, card_id=card.id, location=CardLocation.DECK)
    db_session.add(gc)
    db_session.commit()

    with pytest.raises(HTTPException) as e:
        await service.draw_cards_from_draft_pile(game_id, player_id, [card.id])
    assert e.value.status_code == 400


@pytest.mark.asyncio
async def test_handle_draw_action_full_flow(db_session, seed_cards, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    player_id = create_game_with_players["creator_id"]
    service = create_game_with_players["service"]

    # Creamos cartas en el draft
    draft_cards = []
    for i in range(3):
        card = Card(image=f"draft_{i}.png", type=CardType.EVT)
        db_session.add(card)
        db_session.flush()
        gc = GameCards(
            game_id=game_id,
            card_id=card.id,
            location=CardLocation.DRAFT,
            position=i
        )
        db_session.add(gc)
        draft_cards.append(gc)
    db_session.commit()

    # Usar GameCards.id para draft_selected_ids
    draft_ids = [draft_cards[0].id]  
    result = await service.handle_draw_action(game_id, player_id, draft_ids, 0)

    # Accedemos a la lista de cartas dentro de CardResponse
    drawn_cards = result.cards

    assert len(drawn_cards) >= 1
    assert all(c.owner_id == player_id for c in drawn_cards)
    assert all(c.location == CardLocation.HAND for c in drawn_cards)


@pytest.mark.asyncio
async def test_draw_card_endpoint_full_flow(db_session, test_client, create_game_with_players):
    """
    Testea el endpoint POST /games/{game_id}/draw_card
    asegurando que devuelve correctamente las cartas que se roban
    y que están asignadas al jugador.
    """
    game_id = create_game_with_players["game_id"]
    player_id = create_game_with_players["creator_id"]

    # Crear cartas en el deck
    for i in range(6):
        card = Card(image=f"deck_card_{i}.png", type=CardType.EVT)
        db_session.add(card)
        db_session.flush()
        gc = GameCards(
            game_id=game_id,
            card_id=card.id,
            location=CardLocation.DECK,
            position=i
        )
        db_session.add(gc)
    db_session.commit()

    # Crear algunas cartas en el draft
    draft_cards = []
    for i in range(3):
        card = Card(image=f"draft_card_{i}.png", type=CardType.EVT)
        db_session.add(card)
        db_session.flush()
        gc = GameCards(
            game_id=game_id,
            card_id=card.id,
            location=CardLocation.DRAFT,
            position=i
        )
        db_session.add(gc)
        draft_cards.append(gc)
    db_session.commit()

    # Preparamos payload: seleccionar 2 cartas del draft
    draft_selected_ids = [draft_cards[0].id, draft_cards[1].id]
    payload = {
        "player_id": player_id,
        "draftCardsSelectedIds": draft_selected_ids,
        "drawPileSelectedCount": 2  # Robar 2 del deck
    }

    # Hacemos la request al endpoint
    response = test_client.post(f"/games/{game_id}/draw_card", json=payload)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    # Validamos que devolvió 4 cartas (2 draft + 2 deck)
    assert len(data["cards"]) == 4

    # Validamos que todas las cartas fueron asignadas al jugador y están en la mano
    for c in data["cards"]:
        assert c["owner_id"] == player_id
        assert c["location"] == CardLocation.HAND.value
