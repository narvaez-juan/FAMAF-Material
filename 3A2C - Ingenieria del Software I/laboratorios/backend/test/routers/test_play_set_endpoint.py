from fastapi import status
from models.player_model import Player
import datetime

def test_play_set_poirot_success(test_client, create_game_with_players_and_sets):
    data = create_game_with_players_and_sets
    game_id = data["game_id"]
    creator_id = data["creator_id"]
    poirot_set = next(s for s in data["sets"] if s.get("type") == "HERCULE_POIROT")
    secret_id = data["secrets"][0]["secret_id"]

    response = test_client.post(
        f"/games/process/set/{game_id}",
        json={
            "set_id": poirot_set["set_id"],
            "target_player_id": creator_id,
            "chosen_secret_id": secret_id,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok", "set_play_id": poirot_set["set_id"]}


def test_play_set_poirot_missing_chosen_secret_returns_400(
    test_client, create_game_with_players_and_sets
):
    data = create_game_with_players_and_sets
    game_id = data["game_id"]
    creator_id = data["creator_id"]
    poirot_set = next(s for s in data["sets"] if s.get("type") == "HERCULE_POIROT")

    response = test_client.post(
        f"/games/process/set/{game_id}",
        json={"set_id": poirot_set["set_id"], "target_player_id": creator_id},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # message must match what the service raises for missing chosen_secret_id
    assert response.json() == {"detail": "chosen_secret_id is required for Poirot/Marple"}


def test_play_set_ariadne_pending_selection(test_client, create_game_with_players_and_sets):
    data = create_game_with_players_and_sets
    game_id = data["game_id"]
    creator_id = data["creator_id"]

    ariadne_set = next(s for s in data["sets"] if s.get("type") == "ARIADNE_OLIVER")

    chosen_set_id = data["sets"][0]["set_id"]

    response = test_client.post(
        f"/games/process/set/{game_id}",
        json={
            "set_id": ariadne_set["set_id"],
            "target_player_id": creator_id,
            "chosen_set_id": chosen_set_id,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["status"] == "pending_selection"
    assert body["set_play_id"] == ariadne_set["set_id"]
    assert "message" in body


def test_play_set_game_not_found(test_client, create_game_with_players_and_sets):
    data = create_game_with_players_and_sets
    creator_id = data["creator_id"]
    secret_id = data["secrets"][0]["secret_id"]

    response = test_client.post(
        f"/games/process/set/{5000}",
        json={
            "set_id": 1,
            "target_player_id": creator_id,
            "chosen_secret_id": secret_id,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Game not found"}


def test_play_set_player_not_found(test_client, create_game_with_players_and_sets):
    data = create_game_with_players_and_sets
    game_id = data["game_id"]
    secret_id = data["secrets"][0]["secret_id"]

    response = test_client.post(
        f"/games/process/set/{game_id}",
        json={"set_id": 1, "target_player_id": 190190, "chosen_secret_id": secret_id},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Target player not found"}


def test_play_set_set_not_found(test_client, create_game_with_players_and_sets):
    data = create_game_with_players_and_sets
    game_id = data["game_id"]
    creator_id = data["creator_id"]

    response = test_client.post(
        f"/games/process/set/{game_id}",
        json={"set_id": 11111, "target_player_id": creator_id},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Set not found"}


def test_play_set_unprocessable_content(test_client, create_game_with_players_and_sets):
    data = create_game_with_players_and_sets
    game_id = data["game_id"]
    some_set_id = data["sets"][0]["set_id"]

    response = test_client.post(
        f"/games/process/set/{game_id}",
        json={"set_id": some_set_id, "target_player_id": None},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_play_set_player_not_in_game(db_session, test_client, create_game_with_players_and_sets):
    data = create_game_with_players_and_sets
    game_id = data["game_id"]

    # create a player that belongs to a different game
    player3 = Player(
        name="PlayerNotInGame",
        birthdate=datetime.datetime(2000, 1, 1),
        game_id=99999,
        turn=2,
    )
    db_session.add(player3)
    db_session.commit()
    db_session.refresh(player3)

    some_set_id = data["sets"][0]["set_id"]

    response = test_client.post(
        f"/games/process/set/{game_id}",
        json={"set_id": some_set_id, "target_player_id": player3.id},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Target player does not belong to the game"}
