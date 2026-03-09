from .sockets import sio
from services.game_events import emit_game_list
from db import db_context
from services.card_events import emit_player_secrets


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")


# Room management
@sio.event
async def join_game_list(sid):
    await sio.enter_room(sid, "games:list")
    print(f"Client {sid} joined games:list room")

    # Emit the current game list to the newly joined client
    with db_context() as db:
        await emit_game_list(db)

@sio.event
async def join_game(sid, game_id):
    room_name = f"game:{game_id}"
    await sio.enter_room(sid, room_name)
    print(f"Client {sid} joined {room_name} room")

@sio.event
async def get_game_info(sid, game_id):
    # Emit the current game info to the newly joined client
    with db_context() as db:
        from services.game_events import emit_game_info
        await emit_game_info(game_id, db)

@sio.event
async def get_hand(sid, game_id, player_id):
    # Emit the player_id hand when required
    with db_context() as db:
        from services.card_events import emit_player_hand
        await emit_player_hand(game_id, player_id, db)
        print(f"Client {sid} and id {player_id} request player hand in game {game_id}")

@sio.event
async def get_draw_pile(sid, game_id):
    # Send the draw_pile size
    with db_context() as db:
        from services.card_events import emit_deck_size
        await emit_deck_size(game_id, db)
        print(f"Client {sid} and request deck size in game {game_id}")

@sio.event
async def get_secrets(sid, game_id, player_id):

    with db_context() as db:
        from services.card_events import emit_player_secrets
        await emit_player_secrets(game_id, player_id, db)
        print(f"Sent secrets to player {player_id} in game {game_id}")

@sio.event
async def get_discard_pile(sid, game_id):
    from services.card_events import emit_discard_pile
    with db_context() as db:
        await emit_discard_pile(game_id, db)

@sio.event
async def get_top_discardPile(sid, game_id, player_id, n):

    with db_context() as db:
        from services.card_events import emit_discard_pile
        await emit_discard_pile(game_id, player_id, db, n)
        print(f"Sent top {n} discard pile cards to player {player_id} in game {game_id}")

@sio.event
async def get_player_sets(sid, data):
    player_id = data.get("player_id")
    game_id = data.get("game_id")

    with db_context() as db:
        from services.card_events import emit_player_sets
        await emit_player_sets(game_id, player_id, db)
        print(f"Sent sets to player {player_id} in game {game_id}")

@sio.event
async def get_all_sets(sid, data):

    game_id = data.get("game_id")

    with db_context() as db:
        from services.card_events import emit_all_sets
        await emit_all_sets(game_id, db)
        print(f"Sent all sets in game {game_id}")

@sio.event
async def get_waiting_modal(sid, data):

    game_id = data.get("game_id")
    player_id = data.get("player_id")
    target_player_id = data.get("target_player_id")
    secret_effect = data.get("secret_effect")

    payload = {
        "type": "secret_selection_modal",
        "requester_id": player_id,
        "target_player_id": target_player_id,
        "secret_effect": secret_effect
    }

    await sio.emit("selecting_secret", payload, room=f"game:{game_id}")
    print(f"Notified game {game_id} that player {player_id} is selecting secret for player {target_player_id}")

@sio.event
async def resolve_secret_modal(sid, data):
    game_id = data.get("game_id")
    player_id = data.get("player_id")
    target_player_id = data.get("target_player_id")

    print(f"[sio] Player {player_id} resolved secret for player {target_player_id} in game {game_id}")

    await sio.emit(
        "secret_resolved",
        {
            "type": "secret_reveal_modal",
            "requester_id": player_id,
            "target_player_id": target_player_id,
            "game_id": game_id,
        },
        room=f"game:{game_id}",
    )

@sio.event
async def select_card(sid, data):
    game_id = data.get("game_id")
    player_id = data.get("player_id")
    card_name = data.get("card_name")

    print(f"[sio] Player {player_id} is playing {card_name} in game {game_id}")

    await sio.emit("select_card", data, room=f"game:{game_id}")

@sio.event
async def resolve_select_card(sid, data):
    game_id = data.get("game_id")
    player_id = data.get("player_id")
    card_id = data.get("card_id")
    requester_id = data.get("requester_id")

    print(f"[sio] Player {player_id} selected card:{card_id} in game {game_id} for player:{requester_id}")

    await sio.emit("resolve_select_card_to_requester", data, room=f"game:{game_id}")



@sio.event
async def select_player(sid, data):
    game_id = data.get("game_id")
    player_id = data.get("player_id")
    card_name = data.get("card_name")
   
    print(f"[sio] Player {player_id} is playing {card_name} in game {game_id}")

    await sio.emit("select_player", data, room=f"game:{game_id}")

    
@sio.event
async def resolve_select_player(sid, data):
    game_id = data.get("game_id")
    player_id = data.get("player_id")
    target_player_id = data.get("target_player_id")
    requester_id = data.get("requester_id")

    print(f"[sio] Player {player_id} selected player:{target_player_id} in game {game_id} the requester is {requester_id}")
    await sio.emit("resolve_select_player_to_requester", data, room=f"game:{game_id}")