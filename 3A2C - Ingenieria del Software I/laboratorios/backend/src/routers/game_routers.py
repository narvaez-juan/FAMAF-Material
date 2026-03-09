"""Defines game endpoints."""

import traceback
import os

from db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from services.game_services import GameService, TurnResponse
from services.card_service import CardService
from services.secret_card_service import SecretService
from services.set_services import SetService
from services.effect_cards_events import CardsEventsEffects
from services.action_queue_service import ActionQueueService
from repositories.card_repository import seed_cards_from_json_file
from repositories.secret_card_repository import seed_secrets_from_json_file
from schemas.set_schema import (
    SetIn,
    AriadneJoinRequest,
    StealSet,
    DetectiveJoinRequest
)
from schemas.game_schema import (
    GameIn,
    GameResponse,
    StartGameRequest,
    StartGameResponse,
    DrawCardRequest,
    FinishTurnRequest,
    SecretRequest,
    SecretSteal,
    SetPlayRequest
)
from schemas.player_schema import (
    PlayerIn,
    PlayerResponse
)
from schemas.card_schema import (
    DiscardActionResponse,
    CardResponse,
    CardRequest,
    CardsOffTableRequest,
    DeadCardFollyRequest,
    DelayTheMurdererEscapeRequest,
    AnotherVictimRequest,
    EarlyTrainToPaddingtonRequest,
    LookIntoRequest,
    PointYourSuspicionRequest,
)
from services.exceptions import (
    GameNotFoundError,
    PlayerNotFoundError,
    PlayerNotInGameError,
    SecretNotFoundError,
    SetNotFoundError,
    badRequestError
)

PLAYER_CREATED_GAME = 0

def get_path(*paths):
    for path in paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"None of these paths exist: {paths}")

games_router = APIRouter(prefix="/games")

@games_router.post(path="/create", status_code=status.HTTP_201_CREATED)
async def create_game(game_info: GameIn, db=Depends(get_db)) -> GameResponse:
    """
    creates a new game along with the first player (creator).

    Parameters
    ----------
    game_info : GameIn
        Information about the game to create, including:
            - Game name
            - Minimum and maximum number of players
            - Initial player name
            - Initial player birth date

    db : Session, optional
        Database session provided by FastAPI Depends.

    Returns
    -------
    GameResponse
        game_id : int
            Identifier of the newly created game.
        player_id : int
            Identifier of the player who created the game.

    Raises
    ------
    Conflict
        409 -> If a game with the same name already exists.
    Unprocessable Entity
        422 -> If min_players > max_players, min_players < 2, max_players > 6, or invalid date format.
    Internal Server Error
        500 -> For unexpected errors during game creation or database commit.
    """
    try:
        result = await GameService(db).create_game(game_dto=game_info.to_dto())

        # Get correct path
        cards_path = get_path("src/utils/cards.json", "utils/cards.json")
        secrets_path = get_path("src/utils/secrets_card.json", "utils/secrets_card.json")

        seed_cards_from_json_file(db, cards_path)
        seed_secrets_from_json_file(db, secrets_path)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except Exception as e:
        # Unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
   
    return GameResponse(
        game_id=result[0],
        player_id=result[1]
    )


@games_router.post("/{id_game}/start", response_model=StartGameResponse)
async def start_game(id_game: int, request: StartGameRequest, db=Depends(get_db)):
    """
    starts a game if the requesting player is the creator and the minimum number of players is met.

    Parameters
    ----------
    id_game : int
        The unique identifier of the game to start.
    request : StartGameRequest
        Contains the player_id of the player attempting to start the game.
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    StartGameResponse
        status : str
            "success" if the game started correctly.
        game_id : int
            Identifier of the game that was started.

    Raises
    ------
    Not Found
        404 -> If the game with the given id does not exist.
    Unauthorized
        401 -> If the player is not the creator of the game.
    Not Acceptable
        406 -> If the game does not meet the minimum number of players required.
    Internal Server Error
        500 -> If there are database errors during the commit or event emission.
    """

    service = GameService(db)
    game = await service.start_game_service(id_game, request.player_id)
    return StartGameResponse(status="success", game_id=game)


@games_router.get("/turn/{game_id}", status_code=status.HTTP_200_OK)
async def emit_turn_info(game_id: int, db=Depends(get_db)) -> TurnResponse:
    """
    emits the turn information

    Parameters
    ----------
    game_id : int

    Returns
    -------
    TurnResponse
        Game identifier
        Player turn information
        Game state

    Raises
    ------
    Bad request
        400 -> When the game did not start yet
    Not found
        404 -> When the game is not found
    Internal Server Error
        500 -> Database errors
    """

    try:
        result = await GameService(db).get_turn_info(game_id)
    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return result


@games_router.post("/{game_id}/join", status_code=status.HTTP_201_CREATED)
async def join_game(
    game_id: int, player_info: PlayerIn, db=Depends(get_db)
) -> PlayerResponse:
    """
    allows a player to join an existing game

    Parameters
    ----------
    game_id : int
        Game identifier
    player_info : PlayerIn
        Player information

    Returns
    -------
    PlayerResponse
        Player identifier
        Player name
        Player birthdate

    Raises
    ------
    Bad request
        400 -> When the game is not found or has already started
    Not found
        404 -> When the game is not found
    Internal Server Error
        500 -> Database errors

    Pydantic Errors
    ------
    Error: Unprocessable Content
        422 -> Invalid player information
    """
    try:
        result = await GameService(db).join_game(
            game_id=game_id, player=player_info.to_dto()
        )
    except HTTPException as e:
        # NOTE - Relauch to maintaing original status code
        raise e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        # Unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return result


@games_router.post("/{game_id}/draw_card", status_code=status.HTTP_200_OK)
async def draw_card(game_id: int, request: DrawCardRequest, db=Depends(get_db)
                    ) -> CardResponse:
    """
    updates the game state by drawing cards from the deck to fill 
    the player's hand up to six cards.

    Parameters
    ----------
    game_id : int
        The identifier of the game.
    player_id : int
        The identifier of the player whose hand will be replenished.
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    CardResponse
        cards : List[CardInfo]
            List of card(s) drawn to replenish the player's hand. Each card contains:
                - id: int
                - image: str
                - type: str
                - owner_id: int
                - location: CardLocation("deck", "hand", "discardPile", "draft")
    Raises
    ------
    Not Found
        404 -> If the game or player does not exist.
    Conflict
        409 -> If the deck does not have enough cards to replenish the hand.
    Internal Server Error
        500 -> For unexpected errors during database update or event emission.
    """
    try:
        cards = await GameService(db).handle_draw_action(game_id,request.player_id,request.draftCardsSelectedIds,
                                                         request.drawPileSelectedCount)

        # Check if enough cards were available
        if not cards:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Not enough cards in the deck to replenish the hand"
            )

    except HTTPException:
        # Re-raise known HTTP exceptions
        raise
    except Exception:
        # Unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    return cards


@games_router.post("/{game_id}/discard/{player_id}", response_model=DiscardActionResponse)
async def discard_card_endpoint(game_id: int, player_id: int, request: CardRequest, db=Depends(get_db)):
    """
    Discards one or more cards from a player's hand and updates the game state.  
    The discarded cards are moved to the discard pile, the player's hand is updated, 
    and the turn advances to the next player. Relevant events are emitted to notify 
    the frontend about the updated hand and discard pile.

    Parameters
    ----------
    game_id : int
        The identifier of the game.
    player_id : int
        The identifier of the player discarding cards.
    request : CardRequest
        Object containing the list of card IDs to be discarded.
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    DiscardActionResponse
        game_id : int
            The identifier of the game.
        player_id : int
            The identifier of the player who discarded the cards.
        discarded_cards : List[int]
            List of IDs of the discarded cards.
        updated_hand : List[int]
            List of IDs of the remaining cards in the player's hand after discard.

    Raises
    ------
    Not Found
        404 -> If the game does not exist or a specified card does not belong to the player.
    Bad Request
        400 -> If the game has not started yet or no cards were provided for discard.
    Forbidden
        403 -> If the player attempts to discard when it is not their turn.
    Internal Server Error
        500 -> For unexpected errors during database update or event emission.
    """
    try:
        service = CardService(db)
        response = await service.discard_card(request.card_ids, player_id, game_id)
    except HTTPException:
        # Re-raise known HTTP exceptions
        raise
    except Exception:
        # Unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
    return response


@games_router.post(path="/{game_id}/turn")
async def finish_turn(game_id: int, request: FinishTurnRequest, db=Depends(get_db)):
    """
    Finishes the current player's turn and advances to the next player.

    This endpoint validates whether the requesting player is the one whose turn is currently active. 
    If the validation passes, the game state is updated to reflect the next player's turn, and relevant 
    WebSocket events are emitted to notify all participants of the change.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game.
    request : FinishTurnRequest
        Contains the player_id of the player attempting to finish their turn.
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    int
        The index of the new active turn (based on player order).

    Raises
    ------
    Not Found
        404 -> If the game does not exist or the turn could not be finalized.
    Bad Request
        400 -> If the game has not started yet.
    Forbidden
        403 -> If the player attempts to finish a turn that is not theirs.
    Internal Server Error
        500 -> For unexpected errors during validation, database update, or event emission.
    """

    try:
        result = await GameService(db).finish_turn(game_id, request.player_id)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo finalizar el turno o no se encontró la partida."
            )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

@games_router.post("/update/secret/{game_id}", status_code=status.HTTP_200_OK)
async def update_secret_state(game_id: int, request: SecretRequest, db=Depends(get_db)):
    """
    Reveals or hides a secret card for a player within a game.

    This endpoint updates the `revealed` state of a secret (card) based on the specified effect 
    ("REVEAL" or "HIDE"). After applying the change, it checks whether the player enters or exits 
    social disgrace — a condition that occurs when all of the player's secrets are revealed or when 
    at least one secret becomes hidden again. If the social disgrace state changes, it is updated 
    in the database and broadcasted to all participants in the game via WebSocket.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game.
    request : SecretRequest
        Contains the target player_id, secret_id, and the desired effect ("REVEAL" or "HIDE").
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    dict
        The updated secret data after applying the reveal/hide operation.

    Raises
    ------
    Not Found
        404 -> If the game, player, or secret does not exist.
    Bad Request
        400 -> If the request is malformed or the operation cannot be applied.
    Internal Server Error
        500 -> For unexpected errors during validation, database update, or event emission.
    """
    try:
        service = SecretService(db)
        await service.update_secret_state_service(
            game_id,
            request.player_id, 
            request.secret_id, 
            request.effect)
        
        return {"message": "Secret updated successfully"}

    except GameNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlayerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SecretNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlayerNotInGameError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
    

@games_router.post("/process/set/{game_id}", status_code=status.HTTP_200_OK)
async def process_set(game_id: int, request: SetPlayRequest, db=Depends(get_db)):
    """
    Plays a validated detective set within a game, applying its corresponding effect.
    This endpoint handles the logic for playing an already assembled and validated detective set. 

    Parameters
    ----------
    game_id : int
        The unique identifier of the game.
    request : SetPlayRequest
        Contains the set_id being played, the target_player_id (if any), and optional fields 
        chosen_secret_id or chosen_set_id depending on the detective type.
    db : Session, optional
        Database session injected by FastAPI Depends.

 
    Returns
    -------
    {
        "status": "ok",
        "set_play_id": 123
    }

    or

    {
        "status": "pending_selection",
        "set_play_id": 124,
        "message": "Waiting for target player to choose a secret"
    }

    Raises
    ------
    Not Found
        404 -> If the game, player, or set does not exist.
    Bad Request
        400 -> If required fields are missing.
    Internal Server Error
        500 -> For unexpected errors during effect handling or event emission.
    """

    try:
        service = SetService(db)
        result = await service.play_set(
            game_id,
            request.set_id, 
            request.target_player_id, 
            request.chosen_secret_id,
            request.chosen_set_id)
        
        return result

    except GameNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlayerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SetNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlayerNotInGameError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except badRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

@games_router.post("/steal_secret/{game_id}", status_code=status.HTTP_200_OK)
async def secret_steal(game_id: int, request:SecretSteal, db=Depends(get_db)):
    """
    Steals a secret card from another player within a game.

    This endpoint allows a player to steal a secret (card) that currently belongs to another player 
    in the same game. The operation verifies that both players exist, belong to the given game, 
    and that the target player actually owns the specified secret. If all validations pass, the secret’s 
    ownership is transferred to the stealing player in the database.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game where the stealing takes place.
    request : SecretSteal
        Contains the IDs of the stealing player (`player_id`), 
        the target player (`target_player_id`), 
        and the secret being stolen (`secret_id`).
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    dict
        The updated secret data after stole operation.

    Raises
    ------
    Not Found
        404 -> If the game, either player, or the secret does not exist.
    Bad Request
        400 -> If one of the players does not belong to the specified game.
    Internal Server Error
        500 -> For unexpected errors during validation or database operations.
    """
    try:
        service = SecretService(db)
        await service.steal_secret_service(
            game_id,
            request.player_id,
            request.target_player_id,
            request.secret_id
        )
        
        return {"message": "Secret stolen successfully"}

    except GameNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlayerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SecretNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlayerNotInGameError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
    
@games_router.post("/{game_id}/set/{player_id}/play", status_code=status.HTTP_200_OK)
async def play_set(game_id: int, player_id: int, request: SetIn, db=Depends(get_db)):
    """
    Plays the set for the specified player in the given game.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game.
    player_id : int
        The unique identifier of the player.
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    str
        A message indicating the result of the operation.

    Raises
    ------
    Not Found
        404 -> If the game or player does not exist.
    Bad Request
        400 -> If the game has not started yet or if there are no sets to play.
    Internal Server Error
        500 -> For unexpected errors during database update or event emission.
    """

    try:
        message = await SetService(db).create_set(request.card_ids, player_id, game_id)
        return {"message": message}
    except HTTPException:
        # Re-raise known HTTP exceptions
        raise
    except Exception:
        # Unexpected errors
        print("Unexpected error:", traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
    
@games_router.put("/{game_id}/set/{player_id}/steal", status_code=status.HTTP_200_OK)
async def set_steal(request: StealSet, game_id: int, player_id: int, db=Depends(get_db)):
    """
    Steals a set for the specified player in the given game.

    Parameters
    ----------
    set_id : int
        The unique identifier of the set to steal.
    game_id : int
        The unique identifier of the game.
    player_id : int
        The unique identifier of the player.

    Returns
    -------
    str
        A message indicating the result of the operation.

    Raises
    ------
    Not Found
        404 -> If the game or player does not exist.
    Bad Request
        400 -> If the game has not started yet or if there are no sets to steal.
    Internal Server Error
        500 -> For unexpected errors during database update or event emission.
    """

    try:
        message = await SetService(db).steal_set(game_id, player_id, request.set_id)
        return {"message": message}
    except HTTPException:
        # Re-raise known HTTP exceptions
        raise
    except Exception:
        # Unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

@games_router.post("/ariadne_join_set/{game_id}", status_code=status.HTTP_200_OK)
async def ariadne_join_set(game_id: int, request: AriadneJoinRequest, db=Depends(get_db)):
    """
    Joins an Ariadne card to an existing detective set within a game.

    This endpoint allows a player to attach an Ariadne card to a target detective set,
    re-launching the affect but the owner of the set being the target of the affect of the set. The operation
    validates that the Ariadne card belongs to the player and that the target set exists
    in the specified game.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game.
    request : AriadneJoinRequest
        Contains the ariadne_card_id, target_set_id, and player_id attempting to join the card.
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    dict
        A confirmation message indicating successful join operation.
        Example: {"message": "Ariadne joined set successfully"}

    Raises
    ------
    Not Found
        404 -> If the game, player, card, or set does not exist.
    Bad Request
        400 -> If the Ariadne card cannot be joined to the target set or validation fails.
    Internal Server Error
        500 -> For unexpected errors during database update or event emission.
    """
    try:
        service = SetService(db)
        await service.join_ariadne_to_set(
            game_id=game_id,
            ariadne_card_id=request.ariadne_card_id,
            target_set_id=request.target_set_id,
            player_id=request.player_id,
        )
        return {"message": "Ariadne joined set successfully"}
    except Exception as e:
        # loguear para depuración
        print("Error inesperado en join_ariadne_to_set:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    
@games_router.post("/play/cards-off-table/{game_id}", status_code=status.HTTP_200_OK)
async def endpoint_cards_off_table(game_id:int, request: CardsOffTableRequest, db=Depends(get_db)):
    """
    Plays the "Cards Off the Table" event card for discarding counter cards.

    This endpoint executes the effect of the "Cards Off the Table" card, which forces
    a target player to discard all "Not So Fast..." counter cards from their hand.
    The discarded cards are moved to the discard pile and relevant events are emitted
    to notify all participants in the game.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game where the event is being played.
    request : CardsOffTableRequest
        Contains player_id, id_card (the event card being played), and target_player_id.
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    None
        The endpoint returns HTTP 200 on success without a response body.

    Raises
    ------
    Not Found
        404 -> If the game, player, or card does not exist.
    Bad Request
        400 -> If the action is invalid or the game state does not allow this operation.
    Internal Server Error
        500 -> For unexpected errors discarding 'Not so fast...' cards.
    """
    try:
        service = CardsEventsEffects(db)
        await service.play_cards_off_the_table(
            request.player_id,
            request.id_card,
            request.target_player_id,
            game_id,
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error discarding 'Not so fast...' cards.",
        )

@games_router.post("/play/dead-card-folly/{game_id}", status_code= status.HTTP_200_OK)
async def endpoint_dead_card_folly(game_id:int, request: DeadCardFollyRequest, db=Depends(get_db)):
    """
    Plays the "Dead Card Folly" event card to pass cards between players.

    This endpoint executes the effect of the "Dead Card Folly" card, which allows
    a player to pass a specified number of cards to an adjacent player in the given
    direction (right or left). The operation validates the card ownership,
    updates the hands of affected players, and broadcasts the changes via WebSocket.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game where the event is being played.
    request : DeadCardFollyRequest
        Contains direction (right/left), cards_to_pass (list of card IDs),
        and id_dead_card_folly (the event card being played).
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    None
        The endpoint returns HTTP 200 on success without a response body.

    Raises
    ------
    Not Found
        404 -> If the game, player, or specified cards do not exist.
    Bad Request
        400 -> If the direction is invalid, cards don't belong to the player, or game state disallows the action.
    Internal Server Error
        500 -> For unexpected errors using 'Dead Card Folly...'
    """
    try:
        service = CardsEventsEffects(db)
        await service.play_dead_card_folly(request.direction, request.cards_to_pass,
                                           game_id, request.id_dead_card_folly)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error using 'Dead Card Folly...'"
        )
        
@games_router.post("/play/another_victim/{game_id}/{player_id}", status_code=status.HTTP_200_OK)
async def endpoint_another_victim(
    game_id: int,
    player_id: int,
    request: AnotherVictimRequest,
    db=Depends(get_db),
):
    """
    Plays the "Another Victim" event card for the specified player in the given game.

    This endpoint executes the effect of the "Another Victim" card, allowing the player
    to select a target set and potentially reveal or interact with a secret from another player.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game where the event is being played.
    player_id : int
        The unique identifier of the player who played the "Another Victim" card.
    request : AnotherVictimRequest
            - event_card_id (int): The ID of the event card being played.
            - set_id (int): The ID of the target set affected by the event.
            - secret_id (int): The ID of the chosen secret card (if applicable).
            - target_player_id (int): The ID of the player whose set is targeted.
    db : Session
        The database session dependency.

    Returns
    -------
    dict
        A JSON object indicating successful execution of the effect, including the result payload.
        Example:
        {
            "status": "success",
            "result": { ... }  # contains the effect resolution details
        }

    Raises
    ------
    Not Found
        404 -> If the game, player, or referenced cards do not exist.
    Bad Request
        400 -> If the action is invalid (e.g., illegal target or wrong game state).
    Internal Server Error
        500 -> If an unexpected error occurs during effect execution or database update.
    """
    try:
        service = CardsEventsEffects(db)
        result = await service.play_another_victim(
            game_id=game_id,
            player_id=player_id,
            event_card_id=request.event_card_id,
            target_set_id=request.set_id,
        )

        return {"status": "success", "result": result}

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail="Unexpected error appling the effect for the event card")
    
@games_router.post("/play/delay-murderer-escape/{game_id}", status_code=status.HTTP_200_OK)
async def endpoint_delay_the_murderer_escape(
    game_id:int,
    request:DelayTheMurdererEscapeRequest,
    db=Depends(get_db),
    ):
    """
    Plays the "Delay the Murderer Escape" event card to exchange cards.

    This endpoint executes the effect of the "Delay the Murderer Escape" card, allowing
    a player to take up to five cards from the top of the discard pile and place them on the draw pile in any order, then remove this card from the game.
    The operation validates card ownership, updates player hands, and emits relevant
    WebSocket events to notify all participants.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game where the event is being played.
    request : DelayTheMurdererEscapeRequest
        Contains id_delay_the_murderer_escape (the event card ID), player_id,
        and cards_selected (list of card IDs to exchange).
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    None
        The endpoint returns HTTP 200 on success without a response body.

    Raises
    ------
    Not Found
        404 -> If the game, player, or specified cards do not exist.
    Bad Request
        400 -> If the selected cards are invalid or the game state disallows this operation.
    Internal Server Error
        500 -> For unexpected errors using 'Delay the murderer escape...'
    """
    try:
        service = CardsEventsEffects(db)
        await service.play_delay_the_murderer_escape(
            game_id,
            request.id_delay_the_murderer_escape,
            request.player_id,
            request.cards_selected)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error using 'Delay the murderer escape...'"
        )

@games_router.post("/play/early-train-to-paddington/{game_id}", status_code=status.HTTP_200_OK)
async def endpoint_early_train_to_paddington(
    game_id: int,
    request: EarlyTrainToPaddingtonRequest,
    db=Depends(get_db),
):
    """
    Plays the "Early Train to Paddington" event card to skip the current turn.

    This endpoint executes the effect of the "Early Train to Paddington" card, which
    allows a player to take the top six cards from the draw pile and place them on the discard pile, 
    then removing this card from the game.
    The operation validates that the player is active, updates the game state to
    reflect the turn change, and broadcasts the update via WebSocket.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game where the event is being played.
    request : EarlyTrainToPaddingtonRequest
        Contains player_id and id_early_train_to_paddington (the event card being played).
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    None
        The endpoint returns HTTP 200 on success without a response body.

    Raises
    ------
    Not Found
        404 -> If the game, player, or event card does not exist.
    Bad Request
        400 -> If the game has not started or the player cannot play this card.
    Internal Server Error
        500 -> For unexpected errors using 'Early Train to Paddington' event card.
    """
    try:
        service = CardsEventsEffects(db)
        await service.play_early_train_to_paddington(
            game_id=game_id,
            player_id=request.player_id,
            event_card_id=request.id_early_train_to_paddington,
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error using 'Early Train to Paddington' event card."
        )

@games_router.post("/{game_id}/actions/{action_id}/counter", status_code=status.HTTP_200_OK)
async def play_counter(
    game_id: int,
    action_id: int,
    request: dict,
    db=Depends(get_db)
):
    """
    Play a 'Not So Fast' counter card to interrupt a pending action.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game.
    action_id : int
        The ID of the pending action to counter.
    request : dict
        Request body containing player_id and card_id.
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    dict
        Success status, counter details, and updated timer information.

    Raises
    ------
    Bad Request
        400 -> If counter is invalid (wrong card type, not in hand, expired window, etc.)
    Not Found
        404 -> If action, player, or card not found.
    Internal Server Error
        500 -> For unexpected errors.
    """
    try:
        # Extract from request body
        player_id = request.get("player_id")
        nsf_game_card_id = request.get("card_id")
        
        if not player_id or not nsf_game_card_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="player_id and card_id are required in request body"
            )
        
        action_service = ActionQueueService(db)
        
        result = await action_service.play_counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id,
            game_id=game_id
        )
        
        return {
            "success": True,
            "counter_id": result["counter_id"],
            "chain_position": result["chain_position"],
            "new_expires_at": result["new_expires_at"],
            "message": f"Counter #{result['chain_position']} played. Timer reset to 5 seconds."
        }
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print("Unexpected error in play_counter:", traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    

@games_router.post("/play/look-into-the-ashes/{game_id}/{player_id}", status_code=status.HTTP_200_OK)
async def endpoint_play_look_into_the_ashes(
    game_id: int,
    player_id: int,
    request: LookIntoRequest,
    db=Depends(get_db),
):
    """
    Emits the "Look into the Ashes" event for the specified player in the given game.

    The event notifies all players in the game room that the "Look into the Ashes"
    card has been played, and sends the top cards from the discard pile so that
    the triggering player can view them and select one to recover.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game where the event occurs.
    player_id : int
        The unique identifier of the player who played the "Look into the Ashes" card.
    db : Session
        The database session dependency.
    request: LookIntoRequest
        - event_card_id (int): The ID of the event card being played.
        - chosen_gamecard_id (int): The ID of the card choosed to draft from de discard pile
    
    Returns
    -------
    dict
        A confirmation message indicating that the event was successfully emitted.

        Example:
        {
            "message": "Look into the Ashes event emitted successfully."
        }

    Raises
    ------
    Not Found
        404 -> If the game or player does not exist.
    Internal Server Error
        500 -> If an unexpected error occurs during database access or event emission.
    """

    try:
        service = CardsEventsEffects(db)
        await service.play_look_into_the_ashes(
            game_id=game_id,
            player_id=player_id,
            event_card_id=request.event_card_id,
            chosen_card_id=request.chosen_gamecard_id,
        )
        return {"status": "success"}
    except HTTPException:
        raise
    except Exception:
        import traceback
        print("Error playing 'look into the ashes':", traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error applying 'Look into the ashes' effect",
        )

@games_router.post("/play/point-your-suspicion/{game_id}",status_code = status.HTTP_200_OK)
async def endpoint_point_your_suspision(
    game_id: int,
    request: PointYourSuspicionRequest,
    db=Depends(get_db),
    ):
    """
    Plays the "Point Your Suspicion" event card to reveal information about target players.

    This endpoint executes the effect of the "Point Your Suspicion" card, which makes all the players select another player, 
    the most selected player has to revel a secrete.
    The operation validates the targets, applies the effect,
    and broadcasts the results to all participants via WebSocket.

    Parameters
    ----------
    game_id : int
        The unique identifier of the game where the event is being played.
    request : PointYourSuspicionRequest
        Contains player_id (the player playing the card), target_player_ids (list of targeted players),
        and card_id (the event card being played).
    db : Session, optional
        Database session injected by FastAPI Depends.

    Returns
    -------
    None
        The endpoint returns HTTP 200 on success without a response body.

    Raises
    ------
    Not Found
        404 -> If the game, player, or event card does not exist.
    Bad Request
        400 -> If target players are invalid or the game state disallows this operation.
    Internal Server Error
        500 -> For unexpected errors using 'Point your suspicion' event card.
    """
    try:
        service = CardsEventsEffects(db)
        await service.play_point_your_suspisicion(
            game_id,
            request.player_id,
            request.target_player_ids,
            request.card_id,
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error using 'Point your suspicion' event card."
        )
@games_router.post("/{game_id}/set/{set_id}/detectives", status_code=status.HTTP_200_OK)
async def detective_join_set(game_id: int, set_id: int, request: DetectiveJoinRequest, db=Depends(get_db)):
    """
    Add a Detective card to an existing Set within a game.

    This endpoint allows a player to assign a Detective-type card to an already
    played Set in the specified game. If the operation succeeds, the service
    updates the database and emits the necessary WebSocket events so that
    the game state is refreshed in real time

    Path parameters:
        game_id (int): The ID of the current game.
        set_id (int): The ID of the target Set to which the Detective will be added.

    Request body (DetectiveJoinRequest):
        detective_card_id (int): The ID of the Detective card to be added.
        player_id (int): The ID of the player performing the action.
        target_set_id (int): The ID of the target Set (must match set_id).

    Responses:
        200 OK: The Detective was successfully added to the Set, and all related
                real-time events were emitted. Returns:
                {"status": "ok", "set_play_id": <set_id>}

        400 Bad Request: The Set does not belong to the specified game, or the card
                         does not meet the required conditions.
        404 Not Found:   The Set or Detective card does not exist.
        500 Internal Server Error: Unexpected internal error occurred.

    """
    try:
        service = SetService(db)
        result = await service.join_detective_to_set(
            game_id=game_id,
            detective_card_id=request.detective_card_id,
            target_set_id=set_id,
            player_id=request.player_id,
        )
        return result
    except badRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {e}"
        )