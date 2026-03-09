import enum
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1] 
src = root / "src"
sys.path.insert(0, str(src))

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy.orm import Session
from fastapi import HTTPException
from services.card_events import (
    emit_player_hand,
    emit_discard_pile,
    emit_initial_hand,
    emit_card_draw,
    emit_player_sets,
    emit_all_sets,
    emit_murderer_revealed,
)

class CardType(enum.Enum):
    NSF = "Not so Fast"
    DET = "Detective"
    DEV = "Devious"
    EVT = "Event"

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_sio_emit():
    with patch("services.card_events.sio.emit", new_callable=AsyncMock) as mock_emit:
        yield mock_emit


@pytest.mark.asyncio
async def test_emit_player_hand_emits_hand_payload(mock_db_session, mock_sio_emit):
    gc1 = MagicMock()
    gc1.id = 15
    gc1.card_id = 11
    gc1.card = MagicMock(image="img11.png", type=CardType.DEV)

    gc2 = MagicMock()
    gc2.id = 16
    gc2.card_id = 12
    gc2.card = MagicMock(image="img12.png", type=CardType.EVT)

    # Simular query(...).filter(...).all() -> [gc1, gc2]
    mock_db_session.query.return_value.filter.return_value.all.return_value = [gc1, gc2]

    await emit_player_hand(game_id=5, player_id=42, db=mock_db_session)

    expected_payload = {
        "player_id": 42,
        "cards_list": [
            {"gameCardId": 15, "card_id": 11, "image": "img11.png", "type": "Devious"},
            {"gameCardId": 16, "card_id": 12, "image": "img12.png", "type": "Event"},
        ],
    }

    mock_sio_emit.assert_awaited_once_with("player_hand", expected_payload, room="game:5")


@pytest.mark.asyncio
async def test_emit_discard_pile_orders_and_emits(mock_db_session, mock_sio_emit):
    gc_a = MagicMock(); gc_a.id = 21; gc_a.card = MagicMock(image="a.png", type="trap"); gc_a.discard_order = 2
    gc_b = MagicMock(); gc_b.id = 22; gc_b.card = MagicMock(image="b.png", type="detective"); gc_b.discard_order = 1

    mock_db_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [gc_b, gc_a]

    await emit_discard_pile(game_id=7, db=mock_db_session)

    expected_payload = [
        {"id": 22, "image": "b.png", "type": "detective", "discard_order": 1},
        {"id": 21, "image": "a.png", "type": "trap", "discard_order": 2},
    ]

    mock_sio_emit.assert_awaited_once_with("discard_pile", expected_payload, room="game:7")


@pytest.mark.asyncio
async def test_emit_initial_hand_uses_repos_and_emits(mock_db_session, mock_sio_emit):
    # Preparar players
    player1 = MagicMock(); player1.id = 101
    player2 = MagicMock(); player2.id = 102

    mock_game_repo_inst = MagicMock()
    mock_game_repo_inst.get_players.return_value = [player1, player2]

    # Ahora devolvemos objetos con atributos .id, .image, .type
    card_a1 = MagicMock() 
    card_a1.id = 15
    card_a1.card_id = 1
    card_a1.card = MagicMock(image="img1.png", type=CardType.DET)

    card_a2 = MagicMock()
    card_a2.id = 16
    card_a2.card_id = 2
    card_a2.card = MagicMock(image="img2.png", type=CardType.EVT)

    card_b1 = MagicMock()
    card_b1.id = 17
    card_b1.card_id = 3
    card_b1.card = MagicMock(image="img3.png", type=CardType.EVT)

    mock_gc_repo_inst = MagicMock()
    mock_gc_repo_inst.deal_initial.return_value = None
    mock_gc_repo_inst.get_list_player_game_cards.side_effect = [
        [card_a1, card_a2],  # cartas para player1
        [card_b1],           # cartas para player2
    ]

    with patch("services.card_events.GameRepository") as MockGameRepo, patch(
        "services.card_events.GameCardsRepository"
    ) as MockGCRepo:
        MockGameRepo.return_value = mock_game_repo_inst
        MockGCRepo.return_value = mock_gc_repo_inst

        await emit_initial_hand(game_id=55, db=mock_db_session)

    expected_payload = [
        {
            "player_id": 101,
            "cards_list": [
                {"gameCardId": 15, "card_id": 1, "image": "img1.png", "type": "Detective"},
                {"gameCardId": 16, "card_id": 2, "image": "img2.png", "type": "Event"},
            ],
        },
        {
            "player_id": 102,
            "cards_list": [
                {"gameCardId": 17, "card_id": 3, "image": "img3.png", "type": "Event"},
            ],
        },
    ]

    mock_sio_emit.assert_awaited_once_with("initial_hand", expected_payload, room="game:55")


@pytest.mark.asyncio
async def test_emit_card_draw_success_and_game_not_found(mock_db_session, mock_sio_emit):
    mock_game_repo_inst = MagicMock()
    mock_game = MagicMock(); mock_game.id = 999
    mock_game_repo_inst.get_by_id.return_value = mock_game

    with patch("services.card_events.GameRepository") as MockGameRepo:
        MockGameRepo.return_value = mock_game_repo_inst
        await emit_card_draw(game_id=999, player_id=7, cards_drawn=2, db=mock_db_session)

    expected_payload = {"player_id": 7, "cardsDrawn": 2}
    mock_sio_emit.assert_awaited_once_with("card_draw", expected_payload, room="game:999")

    mock_game_repo_inst.get_by_id.return_value = None
    with patch("services.card_events.GameRepository") as MockGameRepo:
        MockGameRepo.return_value = mock_game_repo_inst
        with pytest.raises(HTTPException) as exc:
            await emit_card_draw(game_id=111, player_id=1, cards_drawn=1, db=mock_db_session)
        assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_emit_player_sets_sucess(mock_db_session, mock_sio_emit):
    gc1 = MagicMock()
    gc1.id = 15
    gc1.card = MagicMock(id=11, image="img11.png")

    gc2 = MagicMock()
    gc2.id = 16
    gc2.card = MagicMock(id=12, image="img12.png")

    sett = MagicMock()
    sett.id = 4
    sett.cards = [gc1, gc2]

    
    # Simular query(...).filter(...).all() -> [sett]
    mock_db_session.query.return_value.filter.return_value.all.return_value = [sett]

    await emit_player_sets(game_id=5, player_id=42, db=mock_db_session)

    expected_payload = {
        "event": "emit_player_sets",
        "player_id": 42,
        "sets": [
            {
             "set_play_id": 4, 
             "card_game_ids": [15, 16], 
             "card_game_images": ["img11.png", "img12.png"],
             "card_types": [11, 12],
             },
        ],
    }

    mock_sio_emit.assert_awaited_once_with("emit_player_sets", expected_payload, room="game:5")


@pytest.mark.asyncio
async def test_emit_player_sets_empty(mock_db_session, mock_sio_emit):
    mock_set_repo = MagicMock()
    mock_set_repo.get_by_player_id.return_value = []

    expected_payload = {
        "event": "emit_player_sets",
        "player_id": 42,
        "sets": []
    }

    await emit_player_sets(game_id=5, player_id=42, db=mock_db_session)

    mock_sio_emit.assert_awaited_once_with("emit_player_sets", expected_payload, room="game:5")


@pytest.mark.asyncio
async def test_emit_all_sets_sucess(mock_db_session, mock_sio_emit):
    gc1 = MagicMock()
    gc1.id = 15
    gc1.card = MagicMock(id=11, image="img11.png")

    gc2 = MagicMock()
    gc2.id = 16
    gc2.card = MagicMock(id=12, image="img12.png")

    sett1 = MagicMock()
    sett1.id = 4
    sett1.owner_id = 101
    sett1.cards = [gc1, gc2]

    sett2 = MagicMock()
    sett2.id = 5
    sett2.owner_id = 102
    sett2.cards = [gc1, gc2]

    player1 = MagicMock(); player1.id = 101
    player2 = MagicMock(); player2.id = 102

    mock_db_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [player1, player2]
    mock_db_session.query.return_value.filter.return_value.all.return_value = [sett1, sett2]

    expected_payload = {
        "event": "player_sets_updated",
        "game_id": 5,
        "players_sets": [
            {
                "player_id": 101,
                "sets": [
                    {
                        "set_play_id": 4,
                        "card_game_ids": [15, 16],
                        "card_game_images": ["img11.png", "img12.png"],
                        "card_types": [11, 12]
                    }
                ]
            },
            {
                "player_id": 102,
                "sets": [
                    {
                        "set_play_id": 5,
                        "card_game_ids": [15, 16],
                        "card_game_images": ["img11.png", "img12.png"],
                        "card_types": [11, 12]
                    }
                ]
            }
        ]
    }


    await emit_all_sets(game_id=5, db=mock_db_session)

    

    mock_sio_emit.assert_awaited_once_with("player_sets_updated", expected_payload, room="game:5")


@pytest.mark.asyncio
async def test_emit_all_sets_empty(mock_db_session, mock_sio_emit):
    mock_set_repo = MagicMock()
    mock_game_repo = MagicMock()
    mock_set_repo.get_by_game_id.return_value = []
    mock_game_repo.get_players.return_value = None

    expected_payload = {
        "event": "player_sets_updated",
        "game_id": 5,
        "players_sets": []
    }

    await emit_all_sets(game_id=5, db=mock_db_session)

    mock_sio_emit.assert_awaited_once_with("player_sets_updated", expected_payload, room="game:5")

@pytest.mark.asyncio
async def test_emit_murderer_revealed_payload(mock_sio_emit):
    await emit_murderer_revealed(
        game_id=99,
        actor_id=7,
        target_id=3,
        secret_id=123,
        secret_name="You're the Murderer!!"
    )

    expected_payload = {
        "game_id": 99,
        "actor_id": 7,
        "target_id": 3,
        "secret_id": 123,
        "secret_name": "You're the Murderer!!"
    }

    mock_sio_emit.assert_awaited_once_with("murderer_revealed", expected_payload, room="game:99")
