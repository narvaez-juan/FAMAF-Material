from models.secret_card_model import Secret, TipoSecreto
from repositories.secret_card_repository import SecretoRepository

def test_create_and_get_secret(db_session):
    repo = SecretoRepository(db_session)

    secret = Secret(
        secret_name="Murderer",
        description="Hidden killer",
        secret_type=TipoSecreto.MURDERER,
        player_id=1,
        game_id=1,
    )

    created = repo.create(secret)
    fetched = repo.get_by_id(created.id)

    assert fetched is not None
    assert fetched.secret_name == "Murderer"
    assert fetched.revealed is False


def test_update_reveal_secret(db_session):
    repo = SecretoRepository(db_session)

    s = Secret(
        secret_name="Accomplice",
        description="Helps the killer",
        secret_type=TipoSecreto.ACCOMPLICE,
        player_id=2,
        game_id=1,
    )
    repo.create(s)

    updated = repo.update_revelate(s.id, True)

    assert updated.revealed is True
    assert repo.get_by_id(s.id).revealed is True


def test_get_all_secrets(db_session):
    repo = SecretoRepository(db_session)
    s1 = Secret(secret_name="S1", secret_type=TipoSecreto.MURDERER, player_id=1, game_id=1)
    s2 = Secret(secret_name="S2", secret_type=TipoSecreto.ACCOMPLICE, player_id=2, game_id=1)

    repo.create(s1)
    repo.create(s2)

    all_secrets = repo.get_all_secrets()
    assert len(all_secrets) == 2
