import pytest
from datetime import datetime
from models.game_model import Game
from models.player_model import Player


def test_emit_turn_info_success(db_session, test_client, create_game_with_players):

    game_id = create_game_with_players["game_id"]

    # Forzar que la partida esté en curso y sincronizar con un jugador existente
    game = db_session.query(Game).filter(Game.id == game_id).first()
    assert game is not None
    jugador2 = Player(
        name="Jugador2", turn=2, game_id=game.id,
        birthdate=datetime(2000, 1, 1), role=None
    )
    jugador3 = Player(
        name="Jugador3", turn=3, game_id=game.id,
        birthdate=datetime(2000, 1, 2), role=None
    )
    db_session.add_all([jugador2, jugador3])
    game.in_game = True
    db_session.commit()

    first_player = db_session.query(Player).filter(Player.game_id == game_id).order_by(Player.turn).first()
    assert first_player is not None
    game.current_turn = first_player.turn
    db_session.commit()

    turn_response = test_client.get(f"/games/turn/{game_id}")
    assert turn_response.status_code == 200
    data = turn_response.json()
    assert data["turnoActual"]["posicionTurno"] == first_player.turn
    assert data["id_partida"] == game_id
    assert any(p["id_jugador"] == first_player.id for p in data["jugadores"])


def test_emit_turn_info_game_not_found(test_client):
    response = test_client.get("/games/turn/99999")
    assert response.status_code == 404
    data = response.json()
    assert "game not found" in data["detail"].lower() or "partida no encontrada" in data["detail"].lower()


def test_emit_turn_info_game_not_started(db_session, test_client, create_game_with_players):
    
    game_id = create_game_with_players["game_id"]

    game = db_session.query(Game).filter(Game.id == game_id).first()
    assert game is not None
    jugador2 = Player(
        name="Jugador2", turn=2, game_id=game.id,
        birthdate=datetime(2000, 1, 1), role=None
    )
    jugador3 = Player(
        name="Jugador3", turn=3, game_id=game.id,
        birthdate=datetime(2000, 1, 2), role=None
    )
    db_session.add_all([jugador2, jugador3])
    game.in_game = False
    db_session.commit()

    turn_response = test_client.get(f"/games/turn/{game_id}")
    assert turn_response.status_code == 400
    data = turn_response.json()
    assert "the game has not started yet" in data["detail"].lower() or "la partida aun no ha comenzado" in data["detail"].lower()


def test_emit_turn_info_single_player(db_session, test_client, create_game_with_players):
    
    game_id = create_game_with_players["game_id"]

    # Dejar la partida con un solo jugador
    game = db_session.query(Game).filter(Game.id == game_id).first()
    game.in_game = True
    players = db_session.query(Player).filter(Player.game_id == game_id).order_by(Player.turn).all()
    for p in players[1:]:
        db_session.delete(p)

    first_player = db_session.query(Player).filter(Player.game_id == game_id).order_by(Player.turn).first()
    assert first_player is not None
    game.current_turn = first_player.turn
    db_session.commit()

    turn_response = test_client.get(f"/games/turn/{game_id}")
    assert turn_response.status_code == 400
    data = turn_response.json()
    assert "not enough players" in data["detail"].lower() or "no hay suficientes jugadores" in data["detail"].lower()
