from fastapi import status
from schemas.game_schema import SecretEffect
from models.player_model import Player
import datetime
    

def test_reveal_secret_success(test_client, create_game_with_players_and_secrets):
    
    game_id = create_game_with_players_and_secrets["game_id"]
    creator_id = create_game_with_players_and_secrets["creator_id"]
    secrets = create_game_with_players_and_secrets["secrets"]

    response = test_client.post(
        f"/games/update/secret/{game_id}", 
        json={
            "player_id": creator_id,
            "secret_id": secrets[0]["secret_id"],
            "effect": SecretEffect.REVEAL.value
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Secret updated successfully"}


def test_reveal_secret_game_not_found(test_client, create_game_with_players_and_secrets):
    
    creator_id = create_game_with_players_and_secrets["creator_id"]
    secrets = create_game_with_players_and_secrets["secrets"]

    response = test_client.post(
        f"/games/update/secret/{5000}", 
        json={
            "player_id": creator_id,
            "secret_id": secrets[0]["secret_id"],
            "effect": SecretEffect.REVEAL.value
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Game not found"}


def test_reveal_secret_player_not_found(test_client, create_game_with_players_and_secrets):
    
    game_id = create_game_with_players_and_secrets["game_id"]
    secrets = create_game_with_players_and_secrets["secrets"]

    response = test_client.post(
        f"/games/update/secret/{game_id}", 
        json={
            "player_id": 190190,
            "secret_id": secrets[0]["secret_id"],
            "effect": SecretEffect.REVEAL.value
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Player not found"}


def test_reveal_secret_secret_not_found(test_client, create_game_with_players_and_secrets):
    
    game_id = create_game_with_players_and_secrets["game_id"]
    creator_id = create_game_with_players_and_secrets["creator_id"]

    response = test_client.post(
        f"/games/update/secret/{game_id}", 
        json={
            "player_id": creator_id,
            "secret_id": 11111,
            "effect": SecretEffect.REVEAL.value
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Secret not found"}


def test_reveal_secret_unnprocessable_content(test_client, create_game_with_players_and_secrets):
    
    game_id = create_game_with_players_and_secrets["game_id"]
    secrets = create_game_with_players_and_secrets["secrets"]


    response = test_client.post(
        f"/games/update/secret/{game_id}", 
        json={
            "player_id": None,
            "secret_id": secrets[0]["secret_id"],
            "effect": SecretEffect.REVEAL.value
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_reveal_secret_player_not_in_game(db_session, test_client, create_game_with_players_and_secrets):
    
    game_id = create_game_with_players_and_secrets["game_id"]
    secrets = create_game_with_players_and_secrets["secrets"]

    # Add third player
    player3 = Player(
        name="Player2",
        birthdate=datetime.datetime(2000, 1, 1),
        game_id=100,
        turn=2
    )
    db_session.add(player3)
    db_session.commit()
    db_session.refresh(player3)

    response = test_client.post(
        f"/games/update/secret/{game_id}", 
        json={
            "player_id": player3.id,
            "secret_id": secrets[0]["secret_id"],
            "effect": SecretEffect.REVEAL.value
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Player does not belong to the game"}