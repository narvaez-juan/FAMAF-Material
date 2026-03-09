import pytest

def test_create_game_success(test_client):
    response = test_client.post(
        "/games/create",
        json={
            "game_name": "prueba2",
            "min_players": 2,
            "max_players": 6,
            "player_name": "Nombre1",
            "player_birth_date": "2025-09-21T00:00:00"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "game_id" in data
    assert "player_id" in data

def test_create_game_invalid_date(test_client):
    response = test_client.post(
        "/games/create",
        json={
            "game_name": "prueba1",
            "min_players": 2,
            "max_players": 6,
            "player_name": "Nombre1",
            "player_birth_date": "ee223dd"
        },
    )
    assert response.status_code == 422

    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert "Input should be a valid date or datetime" in error_detail[0]["msg"]

def test_create_game_empty_fields(test_client):
    response = test_client.post(
        "/games/create",
        json={
            "game_name": "",
            "min_players": 2,
            "max_players": 6,
            "player_name": "",
            "player_birth_date": "2025-09-21"
        },
    )
    assert response.status_code == 422

    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert "String should have at least 1 character" in error_detail[0]["msg"]

def test_create_game_bad_field_type(test_client):
    response = test_client.post(
        "/games/create",
        json={
            "game_name": 123,
            "min_players": "dos",
            "max_players": "seis",
            "player_name": "Jorge",
            "player_birth_date": "2025-09-21"
        },
    )
    assert response.status_code == 422

    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert "Input should be a valid string" in error_detail[0]["msg"]

def test_create_game_minPlayers_greater_than_maxPlayers(test_client):
    response = test_client.post(
        "/games/create",
        json={
            "game_name": "Pedro",
            "min_players": 5,
            "max_players": 4,
            "player_name": "Jorge",
            "player_birth_date": "2025-09-21"
        },
    )
    assert response.status_code == 422

    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert "min_players cannot be greater than max_players" in error_detail[0]["msg"]
    
def test_create_game_minPlayers_maxPlayers_out_of_valid_range(test_client):
    response = test_client.post(
        "/games/create",
        json={
            "game_name": "Pedro",
            "min_players": 1,
            "max_players": 7,
            "player_name": "Jorge",
            "player_birth_date": "2025-09-21"
        },
    )
    assert response.status_code == 422

    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert "Input should be greater than or equal to 2" in error_detail[0]["msg"]