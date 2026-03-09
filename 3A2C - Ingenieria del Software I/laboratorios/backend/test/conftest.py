import datetime
import pytest
from fastapi.testclient import TestClient
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import MagicMock, AsyncMock
from main import app
from db import Base, get_db
# Import models via package path used by the application to avoid duplicate registrations
from models import Card, Game, GameCards, Player
from models.game_cards_model import CardLocation
from models.set_model import SetPlay, SetType, SetEffect
from models.pending_action_model import PendingAction, ActionType, ActionStatus
from services.action_queue_service import ActionQueueService
from repositories.card_repository import seed_cards_from_json_file, get_next_discard_order
from DTOs.game_dto import GameDTO
from services.game_services import GameService
from models.card_model import CardType
from repositories.game_cards_repository import GameCardsRepository
from services.secret_card_service import SecretService
from repositories.secret_card_repository import seed_secrets_from_json_file
from services.secret_card_service import SecretService
from DTOs.secret_dto import SecretDTO, TypeSecret
import pytest_asyncio
import os


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

def get_path(*paths):
    for path in paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"None of these paths exist: {paths}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True, scope="function")
def reset_db():
    """
    Borra y crea todas las tablas antes de cada test.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def test_client():
    """
    Crea un TestClient de FastAPI con override de la dependencia get_db.
    """

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

   
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def seed_cards(db_session):
    
    
    cards_path = get_path("src/utils/cards.json", "utils/cards.json")
    secrets_path = get_path("src/utils/secrets_card.json", "utils/secrets_card.json")

    seed_cards_from_json_file(db_session, cards_path)
    seed_secrets_from_json_file(db_session, secrets_path)


@pytest_asyncio.fixture
async def seed_game_deck(db_session, create_game_with_players, seed_cards):
   
    game_data = create_game_with_players

    repo = GameCardsRepository(db_session)
    repo.seed_game_deck(game_data["game_id"])
    return game_data


@pytest_asyncio.fixture
async def create_game_with_players(db_session):
    service = GameService(db_session)

    game_dto = GameDTO(
        name="TestGame",
        min_players=2,
        max_players=5,
        player_name="Player1",
        player_birth_date=datetime.datetime(2000, 1, 1)
    )
    game_id, creator_id = await service.create_game(game_dto)

    
    player2 = Player(
        name="Player2",
        birthdate=datetime.datetime(2000, 1, 1),
        game_id=game_id,
        turn=2
    )
    db_session.add(player2)
    db_session.commit()
    db_session.refresh(player2)

    return {
        "service": service,
        "game_id": game_id,
        "creator_id": creator_id,
        "player2": player2
    }


@pytest_asyncio.fixture
async def started_game(create_game_with_players, seed_cards):
    service = create_game_with_players["service"]
    game_id = create_game_with_players["game_id"]
    creator_id = create_game_with_players["creator_id"]

    await service.start_game_service(game_id, creator_id)
    return create_game_with_players


@pytest_asyncio.fixture
async def create_player2_card(db_session, create_game_with_players, seed_cards):

    game_id = create_game_with_players["game_id"]
    player2 = create_game_with_players["player2"]

    
    card_base = Card(image="c1.png", type=CardType.EVT)
    db_session.add(card_base)
    db_session.flush()

   
    game_card = GameCards(
        game_id=game_id,
        card_id=card_base.id,
        owner_id=player2.id,
        location=CardLocation.HAND
    )
    db_session.add(game_card)
    db_session.commit()
    db_session.refresh(game_card)

    return game_card


def create_test_game(db, game_id=1):
    """Create a test game with required fields"""
    game = Game(
        id=game_id,
        name="Test Game",
        min_players=2,
        max_players=4,
        players_amount=2,
        in_game=False
    )
    db.add(game)
    db.commit()
    return game

def create_test_card(db, card_id=1):
    """Create a test card with required fields"""
    card = Card(
        id=card_id,
        image=f"card_{card_id}.png",
        type="NSF"  
    )
    db.add(card)
    db.commit()
    return card

def create_card_in_db(db, card_id, game_id=1, position=1, location=CardLocation.DECK, owner_id=None):
    """Create a GameCards entry (association between card and game)"""
    

    card = GameCards(
        card_id=card_id, 
        game_id=game_id, 
        position=position, 
        location=location,
        owner_id=owner_id
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card

@pytest.fixture
def secret_service(db_session):
    """Crea una instancia de SecretService para usar en los tests"""
    return SecretService(db_session)

@pytest_asyncio.fixture
def create_game_with_players_and_secrets(db_session, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    player_id = create_game_with_players["creator_id"]
    player2_id = create_game_with_players["player2"].id
    players = [player_id, player2_id]


    secret_service = SecretService(db_session)
    secret_id_list = []

    for player in players:
        for i in range(3):
            secret_dto = SecretDTO(
                secret_name= "sape",
                description= "sape sape sape sape",
                secret_type= TypeSecret.OTRO,
                player_id=player,
                game_id=game_id,
                revealed= (player != player_id),
                image="sape sape sape sape"
            )

            new_secret = secret_service.create_secret(secret_dto)
            secret_id_list.append({"player_id": player, "secret_id": new_secret.id})
            

    return {
        "game_id": game_id,
        "creator_id": player_id,
        "player2_id": player2_id,
        "secrets": secret_id_list
    }

@pytest_asyncio.fixture
def create_game_with_players_and_murderer_secret(db_session, create_game_with_players):
    game_id = create_game_with_players["game_id"]
    player_id = create_game_with_players["creator_id"]
    player2_id = create_game_with_players["player2"].id
    players = [player_id, player2_id]

    secret_service = SecretService(db_session)
    secret_id_list = []

    for player in players:
        for i in range(3):
            typeSec = TypeSecret.MURDERER if (player == player_id and i == 0) else TypeSecret.OTRO
            secret_dto = SecretDTO(
                secret_name="sape",
                description="sape sape sape sape",
                secret_type=typeSec,
                player_id=player,
                game_id=game_id,
                revealed= (player != player_id),
                image="sape sape sape sape"
            )

            new_secret = secret_service.create_secret(secret_dto)
            secret_id_list.append({
                "player_id": player,
                "secret_id": new_secret.id,
                "secret_type": typeSec.name,
                "secret_name": new_secret.secret_name
            })

    return {
        "game_id": game_id,
        "creator_id": player_id,
        "player2_id": player2_id,
        "secrets": secret_id_list
    }

@pytest_asyncio.fixture
def create_game_with_players_and_sets(db_session, create_game_with_players, create_game_with_players_and_secrets):
    game_id = create_game_with_players["game_id"]
    creator_id = create_game_with_players["creator_id"]
    player2_id = create_game_with_players["player2"].id
    secrets = create_game_with_players_and_secrets["secrets"]

    sets_created = []

    def _create_set(owner_id, set_type, effect, wildcard=False):
        s = SetPlay(
            game_id=game_id,      
            owner_id=owner_id,
            set_type=set_type,
            effect=effect,
            wildcard=wildcard,
        )
        db_session.add(s)
        db_session.commit()
        db_session.refresh(s)
        return s

 
    s1 = _create_set(
        owner_id=creator_id,
        set_type=SetType.HERCULE_POIROT,
        effect=SetEffect.REVEAL_BY_ACTOR,
        wildcard=False,
    )
    
    sets_created.append({"set_id": s1.id, "type": "HERCULE_POIROT", "wildcard": s1.wildcard, "owner_id": creator_id})

  
    s2 = _create_set(
        owner_id=creator_id,
        set_type=SetType.ARIADNE_OLIVER,
        effect=SetEffect.REVEAL_BY_TARGET,
        wildcard=False,
    )
 
    sets_created.append({"set_id": s2.id, "type": "ARIADNE_OLIVER", "wildcard": s2.wildcard, "owner_id": creator_id})

    ariadne_card = Card(image="15-detective_oliver.png", type=CardType.DET)
    db_session.add(ariadne_card)
    db_session.commit()
    db_session.refresh(ariadne_card)

 
    ariadne_game_card = GameCards(
        card_id=ariadne_card.id,
        owner_id=creator_id,   
        game_id=game_id,
        set_id=s2.id
    )
    db_session.add(ariadne_game_card)
    db_session.commit()
    db_session.refresh(ariadne_game_card)


    db_session.refresh(s2)


    s3 = _create_set(
        owner_id=player2_id,
        set_type=SetType.MR_SATTERTHWAITE,
        effect=SetEffect.REVEAL_BY_TARGET,
        wildcard=True,
    )

    sets_created.append({"set_id": s3.id, "type": "MR_SATTERTHWAITE", "wildcard": s3.wildcard, "owner_id": player2_id})


    s4 = _create_set(
        owner_id=player2_id,
        set_type=SetType.PARKER_PYNE,
        effect=SetEffect.HIDE,
        wildcard=False,
    )

    sets_created.append({"set_id": s4.id, "type": "PARKER_PYNE", "wildcard": s4.wildcard, "owner_id": player2_id})

    return {
        "game_id": game_id,
        "creator_id": creator_id,
        "player2_id": player2_id,
        "sets": sets_created,
        "secrets": secrets
    }



# ActionQueueService fixtures
@pytest.fixture
def mock_db_session():
    """Mock database session"""
    return MagicMock()


@pytest.fixture
def mock_action_repo():
    """Mock action repository"""
    return MagicMock()


@pytest.fixture
def mock_game_cards_repo():
    """Mock game cards repository"""
    return MagicMock()


@pytest.fixture
def mock_sio():
    """Mock socket.io instance"""
    return AsyncMock()


@pytest.fixture
def action_queue_service(mock_db_session, mock_action_repo, mock_game_cards_repo, mock_sio):
    """ActionQueueService instance with mocked dependencies"""
    service = ActionQueueService(mock_db_session)
    service.action_repo = mock_action_repo
    service.game_cards_repo = mock_game_cards_repo
    service.sio = mock_sio
    return service


@pytest.fixture
def sample_pending_action():
    """Sample pending action for testing"""
    action = MagicMock(spec=PendingAction)
    action.id = 1
    action.game_id = 1
    action.action_type = ActionType.PLAY_SET
    action.initiator_player_id = 1
    action.target_player_id = 2
    action.status = ActionStatus.PENDING
    action.expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
    action.counters = []
    return action


@pytest.fixture
def sample_nsf_card():
    """Sample NSF card in hand"""
    card = MagicMock(spec=GameCards)
    card.id = 10
    card.owner_id = 2
    card.location = CardLocation.HAND
    card.card = MagicMock()
    card.card.type = CardType.NSF
    card.discard_order = None
    return card