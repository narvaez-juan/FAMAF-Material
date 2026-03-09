from sqlalchemy.orm import Session
from models.game_cards_model import CardLocation
from models.game_cards_model import GameCards
from fastapi import HTTPException,status
from typing import List, Dict
import json
from models.card_model import Card, CardType
from typing import List, Dict
import json

def search_card_by_id(db: Session, card_id: int, player_id: int) -> GameCards:
    card = (
        db.query(GameCards)
        .filter(
            GameCards.card_id == card_id,
            GameCards.owner_id == player_id,
        )
        .first()
    )
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The card was not found or it does not belong to the player"
        )
    return card


def get_next_discard_order(db: Session, game_id: int) -> int:
    last_discard = (
        db.query(GameCards)
        .filter(GameCards.location == CardLocation.DISCARD, GameCards.game_id == game_id)
        .order_by(GameCards.discard_order.desc())
        .first()
    )
    if not last_discard or last_discard.discard_order is None:
        return 1
    return last_discard.discard_order + 1


def normalize_type(t: str) -> CardType:
    """
    Convierte string a CardType (acepta 'NSF','DET','DEV','EVT' mayúsc/minúsc,
    o el value textual como 'Not so Fast'). Lanza ValueError si no coincide.
    """
    if not isinstance(t, str):
        raise ValueError("type must be a string")
    t_up = t.strip().upper()
    if t_up in CardType.__members__:
        return CardType[t_up]
    for ct in CardType:
        if isinstance(ct.value, str) and ct.value.strip().upper() == t_up:
            return ct
    raise ValueError(f"Unknown CardType: {t}")


def card_exists(db: Session, image: str, ctype: CardType) -> bool:
    """Devuelve True si ya existe una Card con la misma image + type."""
    return db.query(Card).filter(Card.image == image, Card.type == ctype).first() is not None


def seed_cards_from_list(
    db: Session,
    records: List[Dict[str, str]],
    skip_if_exists: bool = True
) -> Dict[str, int]:
    processed = inserted = skipped_invalid = already_existing = 0
    to_add = []

    for entry in records:
        processed += 1
        image = entry.get("image")
        t = entry.get("type")
        if not image or not t:
            skipped_invalid += 1
            continue
        try:
            ctype = normalize_type(t)
        except ValueError:
            skipped_invalid += 1
            continue

        if skip_if_exists and card_exists(db, image, ctype):
            already_existing += 1
            continue

        to_add.append(Card(image=image, type=ctype))
        inserted += 1

    if to_add:
        try:
            db.add_all(to_add)
            db.commit()
            for c in to_add:
                try:
                    db.refresh(c)
                except Exception:
                    pass
        except Exception:
            db.rollback()
            raise

    return {
        "processed": processed,
        "inserted": inserted,
        "skipped_invalid": skipped_invalid,
        "already_existing": already_existing,
    }


def seed_cards_from_json_file(
    db: Session,
    json_path: str,
    skip_if_exists: bool = True
) -> Dict[str, int]:
    """
    Carga JSON desde `json_path` (lista de objetos) y llama a seed_cards_from_list.
    """
    with open(json_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, list):
        raise ValueError(
            "JSON root must be a list of objects like { 'image': 'x.png', 'type': 'NSF' }"
        )

    return seed_cards_from_list(db, data, skip_if_exists=skip_if_exists)
