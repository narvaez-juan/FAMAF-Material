from repositories.game_repository import GameRepository
from repositories.player_repository import PlayerRepository
from repositories.game_cards_repository import GameCardsRepository
from repositories.set_repository import SetRepository
from repositories.secret_card_repository import SecretoRepository
from repositories.card_repository import get_next_discard_order
from services.set_services import SetService
from models.game_cards_model import CardLocation, GameCards
from collections import Counter
from .card_events import (
    emit_player_hand,
    emit_discard_pile,
    emit_player_sets,
    emit_player_secrets,
    emit_deck_size,
    emit_card_played_event,
    emit_dead_card_folly_event,
    emit_delay_the_murderer_escape,
    emit_early_train_to_paddington,
    emit_look_into_the_ashes_event,
    emit_another_victim,
    emit_sfp_reveal_secret,
    emit_point_your_suspision,
    point_your_suspicion_effect,
)
from fastapi import HTTPException, status
import random

class CardsEventsEffects:
    
    def __init__(self,db):
        self._db = db
        self.repo_game = GameRepository(db)
        self.repo_player = PlayerRepository(db)
        self.repo_game_cards = GameCardsRepository(db)
        self.repo_set = SetRepository(db)
        self.repo_secret = SecretoRepository(db)

    def check_game(self,game_id:int):
        game = self.repo_game.get_by_id(game_id)
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game or target player not found."
            )
    
    def check_player(self, player_id:int):
        player = self.repo_player.get_player_by_id(player_id)
        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game or target player not found."
            )
    
    def check_target_set(self, target_set_id:int):
        set_target = self.repo_set.get_by_id(target_set_id)
        if not set_target:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or missing target_set_id"
            )

    def check_card(self,id_card,player_id):
        card = self.repo_game_cards.get_by_id(id_card)
        if not card:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="Card not found",
            )
        if card.owner_id != player_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The card is not yours",
            )
    
    def check_secret(self, secret_id: int, player_id: int):
        secret = self.repo_secret.get_by_id(secret_id)
        if not secret:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="Secret card not found"
            )
        if secret.player_id != player_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This secret dont belong to this player",
            )

    def check_player_to_game(self, player_id:int, game_id:int):
        player = self.repo_player.get_player_by_id(player_id)
        if player.game_id != game_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Player {player_id} does not belong to game {game_id}.",
            )

    def change_card_location(self,hands_of_the_target: list[GameCards],game_id:int):
        for card in hands_of_the_target:
            if card.card.image == "16-Instant_notsofast.png":
                card.location = CardLocation.DISCARD
                next_order = get_next_discard_order(self._db, game_id)
                card.owner_id = None
                card.discard_order = next_order
        self._db.commit()

    async def play_cards_off_the_table(
            self,
            player_id:int,
            id_card:int,
            target_player_id:int,
            game_id: int,
        ):
        
        self.check_card(id_card, player_id)
        self.check_player(player_id)
        self.check_game(game_id)
        self.check_player(target_player_id)
        self.check_player_to_game(player_id,game_id)
        self.check_player_to_game(target_player_id,game_id)
        await emit_card_played_event(game_id,player_id,target_player_id)
        
        hands_of_the_target = self.repo_game_cards.get_hand_player(target_player_id)
        self.change_card_location(hands_of_the_target, game_id)

        cards_off_table = self.repo_game_cards.get_card_by_id(id_card)
        cards_off_table.location = CardLocation.DISCARD
        next_order = get_next_discard_order(self._db, game_id)
        cards_off_table.owner_id = None
        cards_off_table.discard_order = next_order

        self._db.commit()
        
        await emit_discard_pile(game_id,self._db)
        await emit_player_hand(game_id,target_player_id,self._db)
        await emit_player_hand(game_id, player_id, self._db)

    
    def check_direction(self,direction:str):
        if (direction != "right") and (direction != "left"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The direction is wrong",
            )
    
    def get_participants(
            self,
            game_id:int,
            cards_to_pass:list[list[int]],
            )->list[int]:
        players = self.repo_game.get_players(game_id)
        ordered_ids = [p.id for p in players]
        participants = [pid for pid in ordered_ids if pid in [p[0] for p in cards_to_pass]]
        return participants

    def calculate_destination_of_the_card(
            self,
            participants:list[int],
            cards_to_pass:list[list[int]],
            direction:str,
            )-> dict:
        new_owners = {}
        amount_of_participants = len(participants)
        for i, player_id in enumerate(participants):
            card_id = next((c for p, c in cards_to_pass if p == player_id), None)
            if not card_id:
                continue
            if direction.lower() == "right":
                new_owner = participants[(i + 1) % amount_of_participants]
            else:
                new_owner = participants[(i - 1) % amount_of_participants]

            new_owners[card_id] = new_owner
        return new_owners


    async def play_dead_card_folly(
            self,direction: str,
            cards_to_pass: list[list[int]],
            game_id:int,
            id_dead_card_folly:int,
            ):
        
        self.check_game(game_id)
        self.check_direction(direction)
        
        cards_to_pass = [pair for pair in cards_to_pass if len(pair) > 1]
        
        for player_id, card_id in cards_to_pass:
            self.check_player(player_id)
            self.check_card(card_id, player_id)
            self.check_player_to_game(player_id,game_id)
        
        dead_card_folly = self.repo_game_cards.get_card_by_id(id_dead_card_folly)
        next_order = get_next_discard_order(self._db, game_id)
        player_id = dead_card_folly.owner_id
        dead_card_folly.location = CardLocation.DISCARD
        dead_card_folly.owner_id = None
        dead_card_folly.discard_order = next_order
        await emit_dead_card_folly_event(game_id,player_id,direction)

        
        participants = self.get_participants(game_id,cards_to_pass)
        if len(participants) < 2:
            return   

        new_owners = self.calculate_destination_of_the_card(participants,cards_to_pass,direction)

        for card_id, new_owner_id in new_owners.items():
            card = self.repo_game_cards.get_card_by_id(card_id)
            card.owner_id = new_owner_id
            card.location = CardLocation.HAND

            if card.card.image == "27-devious_fauxpas.png":
                await emit_sfp_reveal_secret(game_id, new_owner_id, card.id)

        self._db.commit()

        await emit_discard_pile(game_id,self._db)

        for player_id in participants:
            await emit_player_hand(game_id,player_id,self._db)
            
        
    async def play_delay_the_murderer_escape(
            self,
            game_id:int,
            id_delay_the_murderer_escape: int,
            player_id:int,
            cards_selected: list[int],
            ):
        
        self.check_card(id_delay_the_murderer_escape, player_id)
        self.check_game(game_id)
        self.check_player_to_game(player_id,game_id)
        
        await emit_delay_the_murderer_escape(game_id,player_id)

        deck = self.repo_game_cards.get_deck(game_id)
        size_deck = self.repo_game_cards.get_deck_size(game_id)
        if size_deck:
            for card in deck:
                card.position += len(cards_selected)

        for i, card_id in enumerate(cards_selected, start=1):
            card = self.repo_game_cards.get_card_by_id(card_id)
            if not card:
                raise HTTPException(status_code=404, detail=f"Card {card_id} not found")
            if card.location != CardLocation.DISCARD:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="")
            card.location = CardLocation.DECK
            card.owner_id = None
            card.position = i
        
        discard_pile = self.repo_game_cards.get_discard_deck(game_id)
        size_discard_pile = self.repo_game_cards.get_size_discard_deck(game_id)

        if size_discard_pile:
            for card in discard_pile:
                card.discard_order = card.discard_order - len(cards_selected)
        
        self._db.commit()

        delay_the_murderer = self.repo_game_cards.get_card_by_id(id_delay_the_murderer_escape)
        delay_the_murderer.owner_id = None
        delay_the_murderer.location = CardLocation.REMOVED
        delay_the_murderer.discard_order = None

        self._db.commit()

        await emit_discard_pile(game_id,self._db)
        await emit_deck_size(game_id,self._db)
        await emit_player_hand(game_id,player_id,self._db)


    async def play_another_victim(
            self,
            game_id: int,
            player_id: int,
            event_card_id: int,
            target_set_id: int,
    ):
        self.check_card(event_card_id,player_id)
        self.check_player(player_id)
        self.check_game(game_id)
        self.check_target_set(target_set_id)

        await emit_another_victim(game_id,player_id)
        
        target_set = self.repo_set.get_by_id(target_set_id)
        if not target_set:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target set not found"
            )
        
        event_card_played = self.repo_game_cards.get_card_by_id(event_card_id)
        if not event_card_played:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event card not found"
            )

        next_order = get_next_discard_order(self._db,game_id)            
        event_card_played.location = CardLocation.DISCARD
        event_card_played.owner_id = None
        event_card_played.discard_order = next_order

        self._db.commit()

        await emit_discard_pile(game_id,self._db)

        result = target_set

        await emit_player_sets(game_id, player_id, self._db)
        await emit_player_hand(game_id, player_id, self._db)

        return result    


    async def play_early_train_to_paddington(
        self, game_id: int, player_id: int, event_card_id: int,
    ):
        self.check_card(event_card_id, player_id)
        self.check_game(game_id)
        self.check_player_to_game(player_id, game_id)

        await emit_early_train_to_paddington(game_id, player_id)

        draw_pile = self.repo_game_cards.get_deck(game_id)
        top_cards = draw_pile[:6] if draw_pile else []

        next_order = get_next_discard_order(self._db, game_id)
        for card in top_cards:
            card.location = CardLocation.DISCARD
            card.owner_id = None
            card.discard_order = next_order
            next_order += 1

        event_card = self.repo_game_cards.get_card_by_id(event_card_id)
        event_card.location = CardLocation.REMOVED
        event_card.owner_id = None
        event_card.discard_order = None

        self._db.commit()

        await emit_discard_pile(game_id, self._db)
        await emit_deck_size(game_id, self._db)
        await emit_player_hand(game_id, player_id, self._db)
        


    async def play_look_into_the_ashes(
            self,
            game_id: int,
            player_id: int,
            event_card_id: int,
            chosen_card_id: int,
    ):
        
        self.check_game(game_id)
        self.check_player(player_id)
        self.check_card(event_card_id, player_id)
    
        n_discarded = self.repo_game_cards.get_last_n_discarded(game_id, 5)
    
        if not n_discarded:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="There are no cards in the discard pile."
            )
    
        top_discard_cards = [
            {
                "game_card_id": c.id,
                "card_id": c.card_id,
                "image": c.card.image if c.card else None,
                "type": c.card.type if c.card and c.card.type else None,
            }
            for c in n_discarded
        ]
    
        chosen_game_card = next((c for c in n_discarded if c.id == chosen_card_id), None)
    
        if not chosen_game_card:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The chosen card is not among the last discarded cards."
            )
        
        event_card_played = self.repo_game_cards.get_card_by_id(event_card_id)
        if not event_card_played:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event card not found"
            )
        
        try:
            chosen_game_card.owner_id = player_id
            chosen_game_card.location = CardLocation.HAND
            chosen_game_card.discard_order = None

            next_order = get_next_discard_order(self._db,game_id)            
            event_card_played.location = CardLocation.DISCARD
            event_card_played.owner_id = None
            event_card_played.discard_order = next_order
    
            self._db.commit()
    
        except Exception as e:
            self._db.rollback()
            import traceback
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not resolve look into the ashes effect."
            )
        
        try:
            await emit_look_into_the_ashes_event(game_id, player_id, top_discard_cards)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not emit look into the ashes event."
            )
        
        try:
            await emit_discard_pile(game_id, self._db)
            await emit_player_hand(game_id, player_id, self._db)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not emit game updates."
            )
    
    async def play_point_your_suspisicion(
            self,
            game_id:int,
            player_id:int,
            selected_players: list[int],
            event_card_id: int,
    ):

        self.check_card(event_card_id, player_id)
        self.check_game(game_id)
        self.check_player_to_game(player_id, game_id)
        for player in selected_players:
            self.check_player_to_game(player,game_id)
        
        await emit_point_your_suspision(game_id,player_id)
        
        amount_of_repeticion = Counter(selected_players)
        max_repeticiones = max(amount_of_repeticion.values())

        more_frecuency = [player_id for player_id, cant in amount_of_repeticion.items() if cant == max_repeticiones]
        
        player_selected = random.choice(more_frecuency) if len(more_frecuency) > 1 else more_frecuency[0]

        point_your_suspision_card = self.repo_game_cards.get_card_by_id(event_card_id)
        next_order = get_next_discard_order(self._db, game_id)
        player_id = point_your_suspision_card.owner_id
        point_your_suspision_card.location = CardLocation.DISCARD
        point_your_suspision_card.owner_id = None
        point_your_suspision_card.discard_order = next_order

        self._db.commit()

        await emit_player_hand(game_id,player_id,self._db)
        await emit_discard_pile(game_id,self._db)
        await point_your_suspicion_effect(game_id,player_selected, player_id)


        