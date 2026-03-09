"""Game sercvices"""

from fastapi import HTTPException, status

from schemas.game_schema import PlayerTurnInfo, TurnResponse
from schemas.player_schema import PlayerResponse
from schemas.card_schema import CardInfo
from schemas.game_schema import GameFinishReason
from typing import List, Optional
from models.game_model import Game
from DTOs.game_dto import GameDTO
from DTOs.player_dto import PlayerDTO
from models.player_model import Player
from repositories.game_repository import GameRepository
from repositories.game_cards_repository import GameCardsRepository
from repositories.player_repository import PlayerRepository

from fastapi import HTTPException, status
from .game_events import emit_game_list
from .game_events import emit_game_start
from .game_events import emit_game_finished
from .game_events import emit_turn_info_event
from .card_events import emit_card_draw, emit_player_hand, emit_draft_piles
from .card_events import emit_initial_hand
from .card_events import emit_deck_size
from services.game_events import emit_game_info
from repositories.player_repository import search_player_by_id
from .secret_card_service import SecretService
from .card_events import emit_initial_secrets
from models.game_cards_model import GameCards
from schemas.card_schema import CardResponse
from repositories.secret_card_repository import SecretoRepository

MIN_PLAYERS = 2


class GameService:

    def __init__(self, db):
        self._db = db
        # FIXME - Make it equal to the one in card_services, namewise
        self.repo = GameRepository(db)
        self.repo_game_cards = GameCardsRepository(db)
        self.repo_player = PlayerRepository(db)
        self.secret_service = SecretService(db)


    async def create_game(self, game_dto: GameDTO) -> tuple:
        db_game = self.repo.get_by_name(name=game_dto.name)
        if db_game:
            raise ValueError(f"There is a game registered with same name")

        # Create new game
        new_game = Game(
            name=game_dto.name,
            min_players=game_dto.min_players,
            max_players=game_dto.max_players,
            players_amount=1,
            in_game=False,
            current_turn=0,
        )

        self._db.add(new_game)
        self._db.flush()

        # Create new player
        new_player = Player(
            name=game_dto.player_name,
            birthdate=game_dto.player_birth_date,
            game_id=new_game.id,
            # ...Others values in default or NULL
        )

        self._db.add(new_player)

        self._db.commit()

        # Notify clients in the "game_list" room about the new game
        await emit_game_list(self._db)
        self._db.commit()

        return (new_game.id, new_player.id)


    async def join_game(self, game_id: int, player: PlayerDTO) -> Optional[int]:
        game = self.repo.get_by_id(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")

        if game.in_game:
            raise HTTPException(
                status_code=400, detail="Game has already started")

        if game.players_amount == game.max_players:
            raise HTTPException(status_code=400, detail="Game is full")

        new_player = Player(
            name=player.name,
            birthdate=player.birthdate,
            game_id=game.id,
            turn=game.players_amount,
        )

        self._db.add(new_player)
        game.players_amount += 1

        self._db.commit()

        # Notify clients in the "game_list" room about the updated game
        await emit_game_list(self._db)

        return PlayerResponse(
            player_id=new_player.id,
            name=new_player.name,
            birthdate=str(new_player.birthdate),
        )

    async def start_game_service(self, game_id: int, player_id: int) -> int:
        game = self.repo.get_by_id(game_id)

        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Game not found")

        creator_id = game.players[0].id if game.players else None

        if player_id != creator_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You don't have permission to start the game"
            )

        if len(game.players) < MIN_PLAYERS:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="The minimum number of players is not met"
            )

        if game.in_game:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="The game was started"
            )

        # game status
        game.in_game = True
        self._db.commit()
        self._db.refresh(game) 

        # init deck
        self.repo_game_cards.seed_game_deck(game_id)
        self.repo_game_cards.seed_secret_cards(game_id, len(game.players))
        self.repo_game_cards.deal_secrets(game_id,game.players)
        
        self._db.flush()
        self._db.commit()
        
        self._db.commit()
            
        await emit_initial_secrets(game_id,self._db)
            
        # deal all players cards
        await emit_initial_hand(game_id, self._db)

        # notify deck size
        await emit_deck_size(game_id, self._db)

        self.repo_game_cards.seed_draft_piles(game_id)
        self._db.commit()

        await emit_draft_piles(game_id, self._db)

        # notify that game started
        await emit_game_start(game_id, self._db)
        return game.id
    

    async def get_turn_info(self, game_id: int) -> TurnResponse:
        game = self.repo.get_by_id(game_id)
        if not game:
            raise LookupError("Game not found")

        if not game.in_game:
            raise ValueError(f"The game has not started yet")

        players = self.repo.get_players(game_id)
        if len(players) < 2:
            raise ValueError("Not enough players")

        jugadores_info = []
        for player in players:
            jugadores_info.append(
                PlayerTurnInfo(
                    id_jugador=player.id, nombre=player.name, posicionTurno=player.turn
                )
            )

        turno_actual = None
        for jugador in jugadores_info:
            if jugador.posicionTurno == game.current_turn:
                turno_actual = jugador
                break

        await emit_turn_info_event(game_id, self._db, turno_actual, jugadores_info, game.in_game)

        return TurnResponse(
            id_partida=game.id,
            turnoActual=turno_actual,
            jugadores=jugadores_info,
            enCurso=game.in_game,
        )


    async def finish_turn(self, game_id: int, player_id: int) -> int:
        db_game = self.repo.get_by_id(game_id)
        if not db_game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )

        if not db_game.in_game:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The game has not started yet"
            )

        player = search_player_by_id(self._db, player_id, game_id)

        if player.turn != db_game.current_turn:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="It is not your turn"
            )

        # Update game turns
        num_players = len(player.game.players)
        player.game.current_turn = (player.game.current_turn + 1) % num_players
        self._db.commit()

        players = self.repo.get_players(game_id)
        jugadores_info = []
        for player in players:
            jugadores_info.append(
                PlayerTurnInfo(
                    id_jugador=player.id,
                    nombre=str(player.name),
                    posicionTurno=player.turn
                )
            )

        turno_actual_pos = db_game.current_turn
        turno_actual = PlayerTurnInfo(
            id_jugador=players[turno_actual_pos].id,
            nombre=str(players[turno_actual_pos].name),
            posicionTurno=turno_actual_pos
        )

        await emit_game_info(game_id, self._db)
        await emit_turn_info_event(
            game_id, self._db, turno_actual, jugadores_info, db_game.in_game
        )

        return player.game.current_turn
    
    
    async def handle_draw_action(
    self,
    game_id: int,
    player_id: int,
    draft_selected_ids: list[int],
    draw_pile_click_count: int
) -> CardResponse:
        
        game = self.repo.get_by_id(game_id)
        if not game:
                raise HTTPException(status_code=404, detail="Game not found")

        player = self.repo_player.get_player_by_id(player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")

        if player.game_id != game_id:
            raise HTTPException(status_code=400, detail="Player does not belong to the game")

        amount_cards_in_hand = self.repo_game_cards.get_player_cards_in_hand(player_id)
        cards_to_draw = draw_pile_click_count + len(draft_selected_ids)
        cards_can_draw = 6 - amount_cards_in_hand

        if cards_to_draw > cards_can_draw:
            raise HTTPException(status_code=409, detail="Cannot draw more cards than allowed")

        drawn_cards: list[GameCards] = []

        # --- Draft ---
        if draft_selected_ids:
            draft_cards = await self.draw_cards_from_draft_pile(game_id, player_id, draft_selected_ids)
            drawn_cards.extend(draft_cards)

        # --- Deck ---
        if draw_pile_click_count > 0:
            self.repo_game_cards.get_deck_size(game_id)
            deck_cards = await self.draw_cards_from_deck(game_id, player_id, draw_pile_click_count)
            drawn_cards.extend(deck_cards)

        # --- Guardar cambios en DB ---
        try:
            self._db.flush()
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            raise HTTPException(status_code=500, detail="Failed to save card draws") from e

        # --- Emitir eventos ---
        if drawn_cards:
            await emit_player_hand(game_id, player_id, self._db)
            await emit_card_draw(game_id, player_id, len(drawn_cards), self._db)
        await emit_deck_size(game_id, self._db)
        await emit_draft_piles(game_id, self._db)

        # --- Preparar respuesta ---
        card_infos = [
            CardInfo(
                id=c.id,
                image=c.card.image,
                type=c.card.type,
                owner_id=c.owner_id,
                location=c.location
            )
            for c in drawn_cards
        ]

        return CardResponse(cards=card_infos)


    async def draw_cards_from_draft_pile(
        self,
        game_id: int,
        player_id: int,
        selected_ids: list[int]
    ) -> list[GameCards]:
        draft_cards = self.repo_game_cards.get_draft_cards_by_ids(game_id, selected_ids)
        if not draft_cards:
            raise HTTPException(status_code=404, detail="Selected draft cards not found")

        self.repo_game_cards.assign_cards_to_player(draft_cards, player_id)

        # Reponer draft si hace falta
        current_draft_count = self.repo_game_cards.get_draft_count(game_id)
        if current_draft_count < 3:
            missing = 3 - current_draft_count
            self.repo_game_cards.seed_draft_piles(game_id, missing)

        await self.check_handle_endgame(game_id)
        return draft_cards


    async def draw_cards_from_deck(
        self,
        game_id: int,
        player_id: int,
        count: int
    ) -> list[GameCards]:
        game = self.repo.get_by_id(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")

        player = self.repo_player.get_player_by_id(player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")

        cards_drawn = self.repo_game_cards.draw_from_deck(game_id, count)
        self.repo_game_cards.assign_cards_to_player(cards_drawn, player_id)

        await self.check_handle_endgame(game_id)
        return cards_drawn


    async def check_handle_endgame(self, game_id: int) -> None:
        deck_count = self.repo_game_cards.get_deck_size(game_id)
        if deck_count <= 1:
            await emit_game_finished(
                game_id,
                winner_id= SecretoRepository(self._db).get_murder_id(game_id),
                reason=GameFinishReason.MURDERER_ESCAPES,
                db=self._db,
            )
