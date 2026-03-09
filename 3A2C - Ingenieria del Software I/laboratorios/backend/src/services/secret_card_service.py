from repositories.secret_card_repository import SecretoRepository
from models.secret_card_model import Secret
from collections import defaultdict
from typing import Dict
from DTOs.secret_dto import SecretDTO
from realtime.sockets import sio  
from repositories.game_repository import GameRepository
from repositories.player_repository import PlayerRepository
from services.card_events import emit_player_secrets, emit_murderer_revealed
from services.exceptions import (
    GameNotFoundError,
    PlayerNotFoundError,
    PlayerNotInGameError,
    SecretNotFoundError,
    )


class SecretService:
    def __init__(self, db):
        self.repo = SecretoRepository(db)
        self.game_repo = GameRepository(db)
        self.player_repo = PlayerRepository(db)
        self.db = db
        self.sio = sio  


    def group_secrets_by_player(self, all_secrets: list[Secret]) -> Dict[int, list[dict]]:
        grouped = defaultdict(list)
        for secret in all_secrets:
            grouped[secret.player_id].append({
                "id": secret.id,
                "secret_name": secret.secret_name,
                "description": secret.description,
                "type_secret": secret.secret_type.value,
                "revealed": secret.revealed
            })
        return grouped


    def create_secret(self, secret_data: SecretDTO) -> Secret:
        new_secret = secret_data.to_model()
        return self.repo.create(new_secret)


    def reveal_secret(self, secret_id: int, revealed: bool) -> Secret:
        secret = self.repo.update_revelate(secret_id, revealed)
        if not secret:
            raise ValueError("Secret not found")
        return secret
    

    async def update_secret_state_service(self, game_id: int, player_id: int, secret_id: int, effect: str):
        # verify proccedures
        game = self.game_repo.get_by_id(game_id)
        if not game:
            raise GameNotFoundError("Game not found")

        player = self.player_repo.get_player_by_id(player_id)
        if not player:
            raise PlayerNotFoundError("Player not found")

        if player.game_id != game_id:
            raise PlayerNotInGameError("Player does not belong to the game")

        secret = self.repo.get_by_id(secret_id)
        if not secret:
            raise SecretNotFoundError("Secret not found")

        # logic to reveal or hide secret
        reveal = (effect == "REVEAL")

        self.reveal_secret(secret_id, reveal)
        actor = next((p for p in game.players if p.turn == game.current_turn), None)

        if not reveal:
            await self.verify_out_of_social_disgrace(player_id, game_id)
        elif reveal and secret.secret_type.name == "MURDERER":
            await emit_murderer_revealed(game_id, actor.id, player_id, secret.id, secret.secret_name)
        else:
            await self.verify_into_social_disgrace(player_id, game_id)

        await emit_player_secrets(game_id, player_id, self.db)


    async def steal_secret_service(self, game_id: int, player_id: int, target_player_id: int, secret_id: int):

        game = self.game_repo.get_by_id(game_id)
        if not game:
            raise GameNotFoundError("Game not found")
        
        player = self.player_repo.get_player_by_id(player_id)
        if not player:
            raise PlayerNotFoundError("Player not found")
        
        target_player = self.player_repo.get_player_by_id(target_player_id)
        if not target_player:
            raise PlayerNotFoundError("Player not found")

        if player.game_id != game_id or target_player.game_id != game_id:
            raise PlayerNotInGameError("One of the players does not belong to the given game")

        secret = self.repo.get_by_id(secret_id)
        if not secret:
            raise SecretNotFoundError("Secret not found")
        
        if secret.secret_type.name == "MURDERER":
            await emit_murderer_revealed(game_id, player_id, target_player_id, secret.id, secret.secret_name)
        
        self.reveal_secret(secret.id, False)
        updated_secret = self.steal_secret(secret_id, player_id)
        await emit_player_secrets(game_id, player_id, self.db)
        await emit_player_secrets(game_id, target_player_id, self.db)

        return updated_secret

    def steal_secret(self, secret_id: int, new_owner_id: int):
        updated = self.repo.update_secret_owner(secret_id, new_owner_id)
        if not updated:
            raise SecretNotFoundError("Secret not found when trying to steal")
        return updated
    

    async def verify_into_social_disgrace(self, player_id: int, game_id: int):

        secrets = self.repo.get_by_player_id(player_id)
        
        count_revealed = sum(1 for s in secrets if s.revealed)

        if count_revealed == len(secrets):
            # emitir evento de desgracia social
            await self.sio.emit(
                "social_disgrace",
                {"player_id": player_id, "message": "player has revealed all his secrets."},
                room=f"game:{game_id}"
            )


    async def verify_out_of_social_disgrace(self, player_id: int, game_id: int):

        secrets = self.repo.get_by_player_id(player_id)
        
        count_not_revealed = sum(1 for s in secrets if not s.revealed)

        if count_not_revealed == 1:
            # emitir evento de salida de desgracia social
            await self.sio.emit(
                "out_social_disgrace",
                {"player_id": player_id, "message": "player has hidden at least one of his secrets."},
                room=f"game:{game_id}"
            )





