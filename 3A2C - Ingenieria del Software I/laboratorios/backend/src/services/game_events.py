from db import db_context
from sqlalchemy.orm import Session
from repositories.game_repository import GameRepository
from schemas.game_schema import GameFinishReason
from realtime.sockets import sio
from fastapi import HTTPException, status
from schemas.game_schema import PlayerTurnInfo
from models.game_action_model import GameAction, GameActionType

# Game emissions


async def emit_game_list(db):
    repo = GameRepository(db)
    games = repo.get_games()
    game_list = []
    for game in games:
        game_list.append(
            {
                "id": game.id,
                "name": game.name,
                "currentPlayers": game.players_amount,
                "maxPlayers": game.max_players,
            }
        )
    await sio.emit("game_list", game_list, room="games:list")


async def emit_game_start(game_id: int, db):
    repo = GameRepository(db)
    game = repo.get_by_id(game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )
    payload = {"id": game.id, "status": "started"}

    await sio.emit("game_started", payload, room=f"game:{game.id}")


async def emit_player_joined(game_id: int, player_name: str, db):
    repo = GameRepository(db)
    game = repo.get_by_id(game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )
    payload = {"playerName": player_name, "currentPlayers": game.players_amount}

    await sio.emit("player_joined", payload, room=f"game:{game.id}")


async def emit_turn_info_event(
    game_id: int, db, turno_actual: PlayerTurnInfo, jugadores_info: list[PlayerTurnInfo], enCurso: bool
    ):
    repo = GameRepository(db)
    game = repo.get_by_id(game_id)

    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Game not found")
    payload = {
        "turnoActual": turno_actual.model_dump(),
        "jugadores": [j.model_dump() for j in jugadores_info],
        "enCurso": enCurso
    }

    await sio.emit("turn_update", payload, room=f"game:{game.id}")


async def emit_game_info(game_id: int, db):
    repo = GameRepository(db)
    game = repo.get_by_id(game_id)
    players = repo.get_players(game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )
    payload = {
        "id": game.id,
        "name": game.name,
        "currentPlayers": game.players_amount,
        "minPlayers": game.min_players,
        "maxPlayers": game.max_players,
        "status": game.in_game,
        "currentTurn": game.current_turn,
        "players": [
            {"player_id": player.id, "name": player.name, "playerTurn": player.turn} for player in players
        ],
    }

    await sio.emit("game_info", payload, room=f"game:{game.id}")

async def emit_action_event(
    db: Session,
    game_id: int,
    actor_id: int,
    action_type: GameActionType,
    description: str,
    card_id: int = None,
    secret_id: int = None,
):
    payload = {
        "game_id": game_id,
        "actor_id": actor_id,
        "action_type": action_type.value,
        "description": description,
        "card_id": card_id,
        "secret_id": secret_id,
    }
    print("Emitting action_event:", payload)
    await sio.emit("action_event", payload, room=f"game:{game_id}")


async def emit_game_finished(
    game_id: int, winner_id: int, reason: GameFinishReason, db
):
    repo = GameRepository(db)
    game = repo.get_by_id(game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    payload = {
        "type": "game_finished",
        "payload": {"winner_id": winner_id, "reason": reason.value},
    }

    await sio.emit("notify_winner", payload, room=f"game:{game.id}")
