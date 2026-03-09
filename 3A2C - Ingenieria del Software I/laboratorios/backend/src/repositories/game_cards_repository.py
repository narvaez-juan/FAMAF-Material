import random
from typing import List
from sqlalchemy import select
from models.game_cards_model import GameCards
from models.player_model import Player
from models.card_model import Card
from models.game_cards_model import CardLocation
from sqlalchemy.exc import SQLAlchemyError
from models.card_model import CardType
from models.secret_card_model import Secret, TipoSecreto
from random import shuffle
from fastapi import HTTPException

    

# Número de cartas OTRO por cantidad de jugadores
# Diccionario {cantidad de jugadores: cantidad de secretos(OTHER_SECRETS)}
OTRO_COUNT_BY_PLAYERS = {
    2: 5,
    3: 8,
    4: 11,
    5: 13,  # + Murderer + Accomplice
    6: 16,  # + Murderer + Accomplice
}

class GameCardsRepository:

    def __init__(self, db):
        self._db = db

    def get_by_id(self, game_card_id: int):
        return (
             self._db.query(GameCards).filter(GameCards.id == game_card_id).first()
        )
    
    def get_card_by_id(self, game_card_id: int)->GameCards:
        return (
             self._db.query(GameCards).filter(GameCards.id == game_card_id).first()
        )

    def get_player_cards_in_hand(self, player_id: int) -> int:
        """Returns the number of cards a player has in hand"""

        return self._db.query(GameCards).filter(
            GameCards.owner_id == player_id,
            GameCards.location == CardLocation.HAND
        ).count()

    def draw_from_deck(self, game_id: int, n: int) -> list[GameCards]:

        stmt = (
            select(GameCards)
            .where(GameCards.location == CardLocation.DECK, GameCards.game_id == game_id)
            .order_by(GameCards.position)
            .limit(n)
            .with_for_update()
            )
        
        top_cards = self._db.execute(stmt).scalars().all()
        if not top_cards:
            return []

        for cardGame in top_cards:
            cardGame.location = CardLocation.HAND
            
            cardGame.position = None
        self._db.flush()

        remaining_stmt = (
            select(GameCards)
            .where(GameCards.location == CardLocation.DECK, GameCards.game_id == game_id)
            .order_by(GameCards.position)
            .with_for_update()
            )
        
        remaining = self._db.execute(remaining_stmt).scalars().all()
        for index, cardGame in enumerate(remaining, start=1):
            cardGame.position = index
        self._db.flush()

        return top_cards

    def assign_cards_to_player(self, cardGameList: List[GameCards], player_id: int) -> List[GameCards]:
        for cardGame in cardGameList:
            cardGame.owner_id = player_id
        self._db.flush()
        return cardGameList

    def shuffle_deck(self, game_id: int):
            """
            Shuffles the cards with location == DECK and assigns positions from 1 to N randomly.
            This method must be called within a transaction.
            """

            stmt = select(GameCards).where(
                GameCards.location == CardLocation.DECK,
                GameCards.game_id == game_id
            ).with_for_update()

            game_cards = self._db.execute(stmt).scalars().all()
            if not game_cards:
                return []

            positions = list(range(1, len(game_cards) + 1))
            random.shuffle(positions)

            for gameCard, position in zip(game_cards, positions):
                gameCard.position = position

            self._db.flush()
            return game_cards
        
    def deal_initial(self, game_id: int, players: list[Player], per_player: int = 6):
        """
        Deals an initial set of 6 cards to each player.
        players: list of Player objects ordered by turn order.
        """
        # first of all shuffle deck
        self.shuffle_deck(game_id)

        for p in players:
            # assign not so fast card    
            nsf = (
                select(GameCards)
                .where(GameCards.location == CardLocation.DECK, 
                    GameCards.game_id == game_id,
                    GameCards.card_id == 10)  # NSF card id is always 10
                .limit(1)
                .with_for_update()
            )

            nsf_card = self._db.execute(nsf).scalars().first()

            if nsf_card:
                nsf_card.location = CardLocation.HAND
                self.assign_cards_to_player([nsf_card], p.id)

        hands = {p.id: self.get_player_cards_in_hand(p.id) for p in players}

        while any(hands[p.id] < per_player for p in players):
            for p in players:
                if hands[p.id] < per_player:
                    drawn = self.draw_from_deck(game_id, 1)
                    if not drawn:  # deck exhausted
                        return

                    self.assign_cards_to_player(drawn, p.id)
                    hands[p.id] += len(drawn)

        self._db.commit()

    def get_list_player_game_cards(self, player_id: int) -> list[Card]:
        hand_cards = (
            self._db.query(GameCards)
            .filter(GameCards.owner_id == player_id, GameCards.location == CardLocation.HAND)
            .all()
        )

        return hand_cards
    
    def get_hand_player(self, player_id: int) -> list[GameCards]:
        hand_cards = (
            self._db.query(GameCards)
            .filter(GameCards.owner_id == player_id, GameCards.location == CardLocation.HAND)
            .all()
        )

        return hand_cards
    
    def seed_game_deck(self, game_id: int) -> None:
        """
        Create all gameCards row to the new game with game_id
        """
        # get all cards
        cards = self._db.query(Card).filter(Card.type.in_(["DET", "EVT", "NSF", "DEV"])).order_by(Card.id).all()
        if not cards:
            raise ValueError("There is no cards to init deck")

        # create gameCards objects
        to_insert = []
        for card in cards:

            # if is a DET card and is not detective_quinor or detective_oliver
            # then add this card 3 times to make 21 detectives
            if(not ("oliver" in card.image or "quin" in card.image) and card.type == CardType.DET):
                for i in range(3):
                    gc = GameCards(
                    game_id=game_id,
                    card_id=card.id,
                    location=CardLocation.DECK,
                    owner_id=None,
                    discard_order=None,
                    )
                    to_insert.append(gc)
            # if is a DET card and is detective_quin or detective_oliver
            # then add this card 2 times to make 25 detectives
            elif (("oliver" in card.image or "quin" in card.image) and card.type == CardType.DET):
                for i in range(2):
                    gc = GameCards(
                    game_id=game_id,
                    card_id=card.id,
                    location=CardLocation.DECK,
                    owner_id=None,
                    discard_order=None,
                    )
                    to_insert.append(gc)
            # if is a EVT card, add this card 3 times => 27 events cards
            elif (card.type == CardType.EVT):
                for i in range(3):
                    gc = GameCards(
                    game_id=game_id,
                    card_id=card.id,
                    location=CardLocation.DECK,
                    owner_id=None,
                    discard_order=None,
                    )
                    to_insert.append(gc)       
            # if is a DEV card, add this card 2 times => 4 devious cards
            elif (card.type == CardType.DEV):
                for i in range(2):
                    gc = GameCards(
                    game_id=game_id,
                    card_id=card.id,
                    location=CardLocation.DECK,
                    owner_id=None,
                    discard_order=None,
                    )
                    to_insert.append(gc)   
            # if is a DEV card, add this card 10 times => 10 not so fast cards
            elif (card.type == CardType.NSF):
                for i in range(10):
                    gc = GameCards(
                    game_id=game_id,
                    card_id=card.id,
                    location=CardLocation.DECK,
                    owner_id=None,
                    discard_order=None,
                    )
                    to_insert.append(gc)    

        # insert to database
        try:
            self._db.add_all(to_insert)
            self._db.flush()   
            # db.commit() 
        except SQLAlchemyError:
            self._db.rollback()
            raise

    def get_deck_size(self, game_id: int):

        deck_size = self._db.query(GameCards).filter(
                GameCards.location == CardLocation.DECK,
                GameCards.game_id == game_id).count()

        return deck_size
    
    def seed_secret_cards(self, game_id: int, num_players: int) -> None:
        all_secrets= self._db.query(Secret).all()
        if not all_secrets:
            raise ValueError("No hay secretos para inicializar la partida")

        to_insert = []

        # Mezclamos los secretos OTRO para variar
        other_secrets = [s for s in all_secrets if s.secret_type == TipoSecreto.OTRO]
        shuffle(other_secrets)

        # Agregar carta Murderer si corresponde
        if num_players >= 2:
            murderer = next(s for s in all_secrets if s.secret_type == TipoSecreto.MURDERER)
            to_insert.append(
                Secret(
                    secret_name=murderer.secret_name,
                    description=murderer.description,
                    secret_type=murderer.secret_type,
                    image=murderer.image,
                    player_id=None,
                    game_id=game_id,
                    revealed=False
                )
            )

        # Agregar carta Accomplice si corresponde
        if num_players >= 5:
            accomplice = next(s for s in all_secrets if s.secret_type == TipoSecreto.ACCOMPLICE)
            to_insert.append(
                Secret(
                    secret_name=accomplice.secret_name,
                    description=accomplice.description,
                    secret_type=accomplice.secret_type,
                    image=accomplice.image,
                    player_id=None,
                    game_id=game_id,
                    revealed=False
                )
            )

        # Agregar cartas OTRO según cantidad por jugadores
        count_otro = OTRO_COUNT_BY_PLAYERS.get(num_players, 5)
        for i in range(count_otro):
            template = other_secrets[i % len(other_secrets)]
            secret = Secret(
                secret_name=template.secret_name,
                description=template.description,
                secret_type=TipoSecreto.OTRO,
                image=template.image,
                player_id=None,
                game_id=game_id,
                revealed=False
            )
            to_insert.append(secret)

        # Insertar en la base de datos
        try:
            self._db.add_all(to_insert)
            self._db.flush()
            print(f"[Seeder] {len(to_insert)} secret cards created for game {game_id}")
        except SQLAlchemyError as e:
            self._db.rollback()
            print(f"[Seeder] Error creating secrets: {e}")
            raise

    def deal_secrets(self, game_id: int, players: list[Player]):
        secrets = self._db.query(Secret).filter(Secret.game_id == game_id, Secret.player_id == None).all()
        total_needed = len(players) * 3
        if len(secrets) < total_needed:
            raise ValueError(f"No hay suficientes secretos para repartir: {len(secrets)} disponibles, {total_needed} necesarios")
        shuffle(secrets)
        # repartir
        for i, player in enumerate(players):
            player_secrets = secrets[i*3:(i+1)*3]
            for secret in player_secrets:
                secret.player_id = player.id
                secret.revealed = False
        print("Secretos asignados correctamente")  # <-- DEBUG
        self._db.flush()
        self._db.commit()

    def seed_draft_piles(self, game_id: int, n: int = 3):
        """
        Mueve las primeras n cartas del mazo (DECK) al área de DRAFT.
        Reordena el mazo restante manteniendo posiciones consecutivas.
        """
        stmt = (
            select(GameCards)
            .where(GameCards.location == CardLocation.DECK, GameCards.game_id == game_id)
            .order_by(GameCards.position)
            .limit(n)
            .with_for_update()
        )

        top_cards = self._db.execute(stmt).scalars().all()
        if not top_cards:
            return []

        # Cambiar las cartas seleccionadas a DRAFT
        for cardGame in top_cards:
            cardGame.location = CardLocation.DRAFT
            cardGame.owner_id = None
            cardGame.position = None
            cardGame.discard_order = None

        self._db.flush()

        # Reasignar posiciones al resto del mazo
        remaining_stmt = (
            select(GameCards)
            .where(GameCards.location == CardLocation.DECK, GameCards.game_id == game_id)
            .order_by(GameCards.position)
            .with_for_update()
        )
        remaining = self._db.execute(remaining_stmt).scalars().all()
        for index, cardGame in enumerate(remaining, start=1):
            cardGame.position = index

        self._db.flush()
    
    def get_draft_cards_by_ids(self, game_id: int, card_ids: list[int]) -> list[GameCards]:

        if not card_ids:
            return []

        cards = (
            self._db.query(GameCards)
            .filter(
                GameCards.id.in_(card_ids),
                GameCards.game_id == game_id,
                GameCards.location == CardLocation.DRAFT
            )
            .with_for_update()
            .all()
        )

        for card_game in cards:
            card_game.location = CardLocation.HAND
            card_game.position = None

        self._db.flush()

        if len(cards) != len(card_ids):
            invalid_ids = set(card_ids) - {c.id for c in cards}
            raise HTTPException(
                status_code=400,
                detail=f"Cards with game_card_ids={list(invalid_ids)} are not available in draft pile"
            )

        return cards

    def get_draft_count(self, game_id: int) -> int:
        return (
            self._db.query(GameCards)
            .filter(
                GameCards.game_id == game_id,
                GameCards.location == CardLocation.DRAFT
            )
            .count()
        )
    
    def get_draft_cards_by_game(self, game_id: int) -> List[GameCards]:
        return self._db.query(GameCards).filter(
            GameCards.game_id == game_id,
            GameCards.location == CardLocation.DRAFT
        ).all()
    
    def get_cards_for_set(self, card_ids: list[int], owner_id: int, game_id: int) -> list[GameCards]:
        return (
            self._db.query(GameCards)
            .filter(GameCards.id.in_(card_ids), GameCards.owner_id == owner_id, GameCards.game_id == game_id)
            .all()
        )
    
    def get_deck(self,game_id: int) -> list[GameCards]:
        return(
            self._db.query(GameCards)
            .filter(GameCards.game_id == game_id, GameCards.location == CardLocation.DECK)
            .order_by(GameCards.position)
            .all()
        )
    
    def get_discard_deck(self,game_id:int)-> list[GameCards]:
        return (
            self._db.query(GameCards)
            .filter(GameCards.game_id == game_id,GameCards.location == CardLocation.DISCARD)
            .order_by(GameCards.discard_order)
            .all()
        )
    
    def get_size_discard_deck(self, game_id: int)-> int:
        return(
            self._db.query(GameCards)
            .filter(GameCards.game_id == game_id,GameCards.location == CardLocation.DISCARD)
            .count()
        )

    def get_last_n_discarded(self, game_id: int, n: int) -> list[GameCards] | None:
        result = (
            self._db.query(GameCards)
            .filter(GameCards.location == CardLocation.DISCARD, GameCards.game_id == game_id)
            .order_by(GameCards.discard_order.desc())
            .limit(n)
            .all()
        )
        return result if result else []