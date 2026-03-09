import pytest
from fastapi import status
from models.card_model import Card, CardType
from models.game_cards_model import GameCards, CardLocation

# ----------------------------
# Tests
# ----------------------------

@pytest.mark.asyncio
async def test_discard_card_not_your_turn(test_client, db_session, seed_cards, started_game, create_player2_card):
    game_id = started_game["game_id"]
    player2 = started_game["player2"]
    game_card = create_player2_card

    # Llamada al endpoint usando TestClient
    response = test_client.post(
        f"/games/{game_id}/discard/{player2.id}",
        json={"card_ids": [game_card.card_id]}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "It is not your turn"


@pytest.mark.asyncio
async def test_discard_card_card_not_found(test_client, db_session, seed_cards, started_game):
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]

    response = test_client.post(
        f"/games/{game_id}/discard/{creator_id}",
        json={"card_ids": [999]}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "The card was not founded or the card is not yours"


import pytest
from models.card_model import Card, CardType
from models.game_cards_model import GameCards, CardLocation
from fastapi import status

@pytest.mark.asyncio
async def test_discard_multiple_cards_success(test_client, db_session, seed_cards, started_game):
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]

    # Crear varias cartas para el jugador que tiene el turno
    card_names = ["STC", "NTF", "EVT"]
    game_cards = []
    for i, t in enumerate(card_names, 1):
        base_card = Card(image=f"c{i}.png", type=CardType.EVT)
        db_session.add(base_card)
        db_session.flush()

        gc = GameCards(
            game_id=game_id,
            card_id=base_card.id,
            owner_id=creator_id,
            location=CardLocation.HAND
        )
        db_session.add(gc)
        game_cards.append(gc)

    db_session.commit()
    for gc in game_cards:
        db_session.refresh(gc)

    card_ids = [gc.id for gc in game_cards]

    # Hacemos discard usando el mismo jugador que tiene el turno
    response = test_client.post(
        f"/games/{game_id}/discard/{creator_id}",
        json={"card_ids": card_ids}
    )

    assert response.status_code == 200
    data = response.json()
    assert set(data["discarded_cards"]) == set(card_ids)
    assert data["updated_hand"] == []

    # Refrescamos los objetos para que tengan los cambios de la DB
    for cid in card_ids:
        gc = db_session.query(GameCards).filter(GameCards.id == cid).first()
        db_session.refresh(gc)
        # Verificamos que ahora están en la pila de descarte
        assert gc.location == CardLocation.DISCARD
        assert gc.owner_id is None

    db_session.close()


    for cid in card_ids:
        gc = db_session.query(GameCards).filter(GameCards.id == cid).first()
        assert gc.location == CardLocation.DISCARD
        assert gc.owner_id is None


@pytest.mark.asyncio
async def test_discard_card_empty_list(test_client, db_session, seed_cards, started_game):
    game_id = started_game["game_id"]
    creator_id = started_game["creator_id"]

    response = test_client.post(
        f"/games/{game_id}/discard/{creator_id}",
        json={"card_ids": []}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "No cards were provided to discard"


@pytest.mark.asyncio
async def test_discard_card_player_not_found(test_client, db_session, seed_cards, started_game):
    game_id = started_game["game_id"]

    response = test_client.post(
        f"/games/{game_id}/discard/999",
        json={"card_ids": [1]}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "the player does not exist"


@pytest.mark.asyncio
async def test_discard_card_game_not_found(test_client, db_session, seed_cards):
    response = test_client.post(
        f"/games/999/discard/1",
        json={"card_ids": [1]}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Game not found"


@pytest.mark.asyncio
async def test_discard_card_game_not_started(test_client, db_session, seed_cards, create_game_with_players, create_player2_card):
    game_id = create_game_with_players["game_id"]
    creator_id = create_game_with_players["creator_id"]
    game_card = create_player2_card

    response = test_client.post(
        f"/games/{game_id}/discard/{creator_id}",
        json={"card_ids": [game_card.card_id]}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "The game has not started yet"
