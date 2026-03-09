"""Repositorio para manejar operaciones con secretos."""
from sqlalchemy.orm import Session
import json
from typing import List, Dict
from sqlalchemy.exc import SQLAlchemyError
from models.secret_card_model import Secret, TipoSecreto


class SecretoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, secret):
        self.db.add(secret)
        self.db.commit()
        self.db.refresh(secret)
        return secret
        
    def get_by_id(self, secreto_id: int) -> Secret | None:
        return self.db.query(Secret).filter(Secret.id == secreto_id).first()

    def get_murder_id(self, game_id: int) -> int:
       secret = (
            self.db.query(Secret)
            .filter(
                Secret.game_id == game_id,
                Secret.secret_type == "Murderer",
            )
            .first()
        )
       return secret.player_id if secret else None


    def update_revelate(self, secret_id: int, revealed: bool) -> Secret | None:
        secret = self.get_by_id(secret_id)
        if secret:
            secret.revealed = revealed
            self.db.commit()
            self.db.refresh(secret)
        return secret
    
    def get_all_secrets(self) -> list[Secret]:
        return self.db.query(Secret).all()
    
    def get_by_game_id(self, game_id: int) -> list[Secret]:   
        return (
            self.db.query(Secret)
            .filter(Secret.game_id == game_id)
            .all()
        )
    
    def get_by_player_id(self, player_id: int) -> list[Secret]:
        return (
            self.db.query(Secret)
            .filter(Secret.player_id == player_id)
            .all()
        )

    def update_secret_owner(self, secret_id: int, new_player_id: int):
        secret = self.get_by_id(secret_id)
        if secret:
            secret.player_id = new_player_id
            self.db.commit()
            self.db.refresh(secret)
        return secret


def normalize_secret_type(t: str) -> TipoSecreto:
    """
    Convierte string a TipoSecreto (acepta 'MURDERER', 'ACCOMPLICE', 'OTRO'
    o el value textual como 'Murderer'). Lanza ValueError si no coincide.
    """
    if not isinstance(t, str):
        raise ValueError("type_secret must be a string")
    t_up = t.strip().upper()
    if t_up in TipoSecreto.__members__:
        return TipoSecreto[t_up]
    for ts in TipoSecreto:
        if isinstance(ts.value, str) and ts.value.strip().upper() == t_up:
            return ts
    raise ValueError(f"Unknown TipoSecreto: {t}")


def secret_exists(db: Session, secret_name: str, secret_type: TipoSecreto) -> bool:
    """Devuelve True si ya existe un Secret con el mismo nombre y tipo."""
    return (
        db.query(Secret)
        .filter(Secret.secret_name == secret_name, Secret.secret_type == secret_type)
        .first()
        is not None
    )


def seed_secrets_from_list(
    db: Session,
    records: List[Dict[str, str]],
    skip_if_exists: bool = True
) -> Dict[str, int]:
    """
    Inserta cartas secretas base desde una lista de diccionarios.
    Cada registro debe tener: 'secret_name', 'secret_type'.
    """
    processed = inserted = skipped_invalid = already_existing = 0
    to_add = []

    for entry in records:
        processed += 1
        name = entry.get("secret_name")
        t = entry.get("secret_type")

        if not name or not t:
            skipped_invalid += 1
            continue

        try:
            secret_type = normalize_secret_type(t)
        except ValueError:
            skipped_invalid += 1
            continue

        if skip_if_exists and secret_exists(db, name, secret_type):
            already_existing += 1
            continue

        to_add.append(
            Secret(
                secret_name=name,
                description=entry.get("description", ""),
                image=entry.get("image", ""),
                secret_type=secret_type,
                revealed=False,
            )
        )
        inserted += 1

    if to_add:
        try:
            db.add_all(to_add)
            db.commit()
            for s in to_add:
                try:
                    db.refresh(s)
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



def seed_secrets_from_json_file(
    db: Session,
    json_path: str,
    skip_if_exists: bool = True
) -> Dict[str, int]:
    """
    Carga JSON desde `json_path` (lista de objetos) y llama a seed_secrets_from_list.
    """
    with open(json_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, list):
        raise ValueError(
            "JSON root must be a list de objetos como: "
            "{ 'secret_name': 'Eres el asesino', 'secret_type': 'Murderer' }"
        )

    return seed_secrets_from_list(db, data, skip_if_exists=skip_if_exists)
