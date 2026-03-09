from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.game_cards_model import CardLocation
from realtime.sockets import sio
from repositories.game_repository import GameRepository
from repositories.game_cards_repository import GameCardsRepository
from repositories.set_repository import SetRepository
from models.game_cards_model import GameCards, CardLocation
from models.secret_card_model import Secret
from models.set_model import SetPlay, SetType


async def emit_player_hand(game_id: int, player_id: int, db: Session):
    hand_cards = (
        db.query(GameCards)
        .filter(GameCards.owner_id == player_id, GameCards.location == CardLocation.HAND)
        .all()
    )

    hand_payload = []
    card_list = []
    for gc in hand_cards:
        card_list.append(
            {
                "gameCardId": gc.id,
                "card_id": gc.card_id,
                "image": gc.card.image,
                "type": gc.card.type.value,
            }
        )
    
    hand_payload = {
        "player_id": player_id,
        "cards_list": card_list 
    }

    await sio.emit("player_hand", hand_payload, room=f"game:{game_id}")

async def emit_discard_pile(game_id: int, db: Session):
    # Traemos todas las cartas descartadas de la partida
    discarded = (
        db.query(GameCards)
        .filter(GameCards.game_id == game_id, GameCards.location == CardLocation.DISCARD)
        .order_by(GameCards.discard_order.asc())
        .all()
    )

    discard_payload = []
    for gc in discarded:
        discard_payload.append(
            {
                "id": gc.id,
                "image": gc.card.image,  # accedemos a la carta real
                "type": gc.card.type,
                "discard_order": gc.discard_order
            }
        )

    await sio.emit("discard_pile", discard_payload, room=f"game:{game_id}")

async def emit_top_discard_pile(game_id: int, player_id: int, db: Session, n: int):
    
    from repositories.game_cards_repository import GameCardsRepository
    repo_game_cards = GameCardsRepository(db)
    top_discard_pile = repo_game_cards.get_last_n_discarded(game_id, n)

    if not top_discard_pile:
        print(f"There is not discarded cards in the pile in game {game_id}")
        await sio.emit(
            "top_discard",
            {
                "player_id": player_id,
                "top_discard_cards": []
            },
            room=f"game:{game_id}"
        )
    
    top_discard_cards = []
    for gc in top_discard_pile:
        top_discard_cards.append(
            {
                "gameCardId": gc.id,
                "card_id": gc.card_id,
                "image": gc.card.image,
                "type": gc.card.type.value, 

            }
        )

    discard_payload = {
            "player_id": player_id,
            "top_discard_cards": top_discard_cards,
            "total_cards": len(top_discard_cards)
        }
    
    await sio.emit("top_discard", discard_payload, room=f"game:{game_id}")

async def emit_initial_hand(game_id: int, db: Session):

    gameRepo = GameRepository(db)
    gameCardsepo = GameCardsRepository(db)

    player_list = gameRepo.get_players(game_id)

    # Initial dealing for all players - giving all players cards
    gameCardsepo.deal_initial(game_id, player_list)

    hand_payload = []

    for player in player_list:
        player_game_cards_list = gameCardsepo.get_list_player_game_cards(player.id)

        card_list = []
        for gc in player_game_cards_list:
            card_list.append(
                {
                    "gameCardId": gc.id,
                    "card_id": gc.card_id,
                    "image": gc.card.image,
                    "type": gc.card.type.value, 
                }
            )

        hand_payload.append(
            {
                "player_id": player.id,
                "cards_list": card_list
            }
        )

    await sio.emit("initial_hand",hand_payload, room=f"game:{game_id}")

async def emit_card_draw(game_id: int, player_id: int, cards_drawn: int, db):
    repo = GameRepository(db)
    game = repo.get_by_id(game_id)

    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Game not found")
    payload = {
        "player_id": player_id,
        "cardsDrawn": cards_drawn
    }

    await sio.emit("card_draw", payload, room=f"game:{game.id}")

async def emit_deck_size(game_id: int, db):
    repo1 = GameRepository(db)
    game = repo1.get_by_id(game_id)

    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Game not found")
    
    repo = GameCardsRepository(db)
    count = repo.get_deck_size(game_id)

    payload = {"deck_size": count}

    await sio.emit("draw_pile", payload, room=f"game:{game.id}")

async def emit_initial_secrets(game_id: int, db: Session):
    """
    Emite las cartas secretas iniciales de cada jugador de una partida.
    Rompe si no hay jugadores o no hay secretos asignados.
    """
    #obtener los jugadores que tienen secretos en esta partida
    player_ids = [s.player_id for s in db.query(Secret.player_id)
                  .filter(Secret.game_id == game_id)
                  .distinct()
                  .all()]

    if not player_ids:
        # No hay jugadores con secretos: falla explícitamente
        raise ValueError(f"No players with secrets found for game {game_id}")

    hand_payload = []
    #obtengo los secretos de cada jugador
    for player_id in player_ids:
        player_secrets = db.query(Secret).filter(
            Secret.game_id == game_id,
            Secret.player_id == player_id
        ).all()

        if not player_secrets:
            raise ValueError(f"Player {player_id} in game {game_id} has no secrets assigned")

        secret_list = []
        for s in player_secrets:
            secret_list.append(
                {
                    "id": s.id,
                    "name": s.secret_name,
                    "description": s.description,
                    "type": s.secret_type.value,
                    "image": s.image,
                }
            )

        hand_payload.append(
            {
                "player_id": player_id,
                "secrets_list": secret_list
            }
        )

    # Emitimos a la room de la partida
    await sio.emit("initial_secrets", hand_payload, room=f"game:{game_id}")

async def emit_player_secrets(game_id: int, player_id: int, db: Session):

    player_secrets = db.query(Secret).filter(
        Secret.game_id == game_id,
        Secret.player_id == player_id
    ).all()

    if not player_secrets:
        print(f"Player {player_id} in game {game_id} has no secrets assigned")
        return

    secrets_list = []
    for s in player_secrets:
        secrets_list.append(
            {
                "id": s.id,
                "name": s.secret_name,
                "description": s.description,
                "type": s.secret_type.value,
                "image": s.image,
                "isRevealed": getattr(s, "revealed", False)
            }
        )

    payload = {
        "player_id": player_id,
        "secrets_list": secrets_list
    }

    await sio.emit("player_secrets", payload, room=f"game:{game_id}")

async def emit_murderer_revealed(game_id: int, actor_id: int, target_id: int, secret_id: int, secret_name: str):
    
    payload = {
        "game_id": game_id,
        "actor_id": actor_id,
        "target_id": target_id,
        "secret_id": secret_id,
        "secret_name": secret_name,
    }

    await sio.emit("murderer_revealed", payload, room=f"game:{game_id}")

async def emit_draft_piles(game_id: int, db: Session):
    gameCardsepo = GameCardsRepository(db)
    draft_cards = gameCardsepo.get_draft_cards_by_game(game_id)
    payload = {
        "draft_cards": [
            {
                "id": gc.id,
                "image": gc.card.image,
                "type": gc.card.type
            } for gc in draft_cards
        ]
    }
    await sio.emit("draft_piles", payload, room=f"game:{game_id}")

async def emit_player_sets(game_id: int, player_id: int, db: Session):
    setPlayRepo = SetRepository(db)
    player_sets = setPlayRepo.get_by_player_id(game_id, player_id)

    if not player_sets:
        print(f"There is not Sets for this player: {player_id} in game: {game_id}")
        await sio.emit("emit_player_sets", {
            "event": "emit_player_sets",
            "player_id": player_id,
            "sets": []
        }, room=f"game:{game_id}")
        return

    setList = []

    for sett in player_sets:
        gamesCard = []
        gamesCardIdList = []
        gamesCardImages = []
        gamesCardTypes = []

        gamesCard = sett.cards
        
        for gameCard in gamesCard:
            gamesCardIdList.append(gameCard.id) 
            gamesCardImages.append(gameCard.card.image)
            gamesCardTypes.append(gameCard.card.id)
            
        setList.append(
            {
                "set_play_id": sett.id,
                "card_game_ids": gamesCardIdList,
                "card_game_images": gamesCardImages,
                "card_types": gamesCardTypes
            }
        )
    
    payload = {
        "event": "emit_player_sets",
        "player_id": player_id,
        "sets": setList
    }

    await sio.emit("emit_player_sets", payload, room=f"game:{game_id}")

async def emit_all_sets(game_id: int, db: Session):
    setPlayRepo = SetRepository(db)
    gameRepo = GameRepository(db)

    players = gameRepo.get_players(game_id)
    allSets = setPlayRepo.get_by_game_id(game_id)

    if not allSets:
        print(f"There is not Sets in game: {game_id}")
        await sio.emit("player_sets_updated", 
                       {
                            "event": "player_sets_updated",
                            "game_id": game_id,
                            "players_sets": []
                        }, 
                       room=f"game:{game_id}")

    AllSetsList = []

    for player in players:

        playerSets = list(filter(lambda x: x.owner_id == player.id, allSets))
        setList = []

        for sett in playerSets:
            gamesCard = []
            gamesCardIdList = []
            gamesCardImages = []
            gamesCardTypes = []

            gamesCard = sett.cards
            
            for gameCard in gamesCard:
                gamesCardIdList.append(gameCard.id) 
                gamesCardImages.append(gameCard.card.image)
                gamesCardTypes.append(gameCard.card.id)
                
            setList.append(
                {
                    "set_play_id": sett.id,
                    "card_game_ids": gamesCardIdList,
                    "card_game_images": gamesCardImages,
                    "card_types": gamesCardTypes
                }
            )

        AllSetsList.append( 
            {
                "player_id": player.id,
                "sets": setList
            })
        
    payload = {
        "event": "player_sets_updated",
        "game_id": game_id,
        "players_sets": AllSetsList
    }

    await sio.emit("player_sets_updated", payload, room=f"game:{game_id}")

async def emit_set_effects(set_play: SetPlay, game_id: int, cards_ids: list[int]):
    """Emit events based on the set effects."""
    type = set_play.set_type

    payload = {
        "owner_id": set_play.owner_id,
        "set_type": type,
        "cards": cards_ids,
    }

    if type in {SetType.HERCULE_POIROT, SetType.MISS_MARPLE}:
        # Reveal by actor
        await sio.emit("owner_chooses_secret", payload, room=f"game:{game_id}")
    else:
        # Reveal by target
        await sio.emit("target_chooses_secret", payload, room=f"game:{game_id}")


async def emit_card_played_event(
    game_id: int,
    player_id: int,
    target_player_id: int,
):
    payload = {
        "event": "card_played_event",
        "game_id": game_id,
        "player_id": player_id,
        "target_player_id": target_player_id,
        "card_name": "Cards Off The Table",
        "card_type": "Event"
    }

    await sio.emit("card_played_event", payload, room=f"game:{game_id}")

async def emit_dead_card_folly_event(game_id: int, player_id: int, direction: str):

    payload = {
        "event": "dead_card_folly_event",
       "game_id": game_id,
        "player_id": player_id,
        "card_name": "Dead Card Folly",
        "card_type": "Event",
        "direction": direction.lower()  # 'left' o 'right'
    }

    await sio.emit("card_played_event", payload, room=f"game:{game_id}")

async def emit_delay_the_murderer_escape(game_id:int, player_id:int):

    payload = {
        "event": "card_played_event",
        "game_id": game_id,
        "player_id": player_id,
        "card_name": "Delay the Murderer’s Escape!",
        "card_type": "Event"
    }

    await sio.emit("card_played_event", payload, room=f"game:{game_id}")

async def emit_early_train_to_paddington(game_id: int, player_id: int):

    payload = {
        "event": "early_train_to_paddington",
        "game_id": game_id,
        "player_id": player_id,
        "card_name": "Early Train to Paddington",
        "card_type": "Event"
    }
    
    await sio.emit("card_played_event", payload, room=f"game:{game_id}")

async def emit_look_into_the_ashes_event(game_id: int, player_id: int, top_discard_cards: list):

    payload = {
        "event": "look_into_the_ashes_event",
        "game_id": game_id,
        "player_id": player_id,
        "card_name": "Look into the Ashes",
        "card_type": "Event",
        "top_discard_cards": top_discard_cards,
    }

    await sio.emit("card_played_event", payload, room=f"game:{game_id}")


async def emit_sfp_reveal_secret(game_id: int, player_id: int, card_id: int):
    payload = {
        "event": "sfp_reveal_secret",
        "game_id": game_id,
        "player_id": player_id,
        "source_card": "Social Faux Pas",
        "card_id": card_id
    }
    await sio.emit("sfp_reveal_secret", payload, room=f"game:{game_id}")


async def emit_another_victim(game_id: int, player_id: int):

    payload = {
        "event": "antoher_victim",
        "game_id": game_id,
        "player_id": player_id,
        "card_name": "Another Victim",
        "card_type": "Event"
    }
    
    await sio.emit("card_played_event", payload, room=f"game:{game_id}")

async def point_your_suspicion_effect(game_id:int,player_selected: int, player_id: int):
    payload = {
        "event": "card_played_event",
        "game_id": game_id,
        "card_name": "Point Your Suspicion",
        "card_type": "Event",
        "player_id": player_id,
        "target_player_id": player_selected
    }
    await sio.emit("card_played_event", payload, room=f"game:{game_id}")

async def emit_point_your_suspision(game_id: int, player_id: int):
    payload = {
        "event": "card_played_event",
        "game_id": game_id,
        "card_name": "Point Your Suspicion",
        "card_type": "Event",
        "player_id": player_id
    }
    await sio.emit("card_played_event", payload, room=f"game:{game_id}")