
class GameServiceError(Exception):
    pass

class GameNotFoundError(GameServiceError):
    pass

class PlayerNotFoundError(GameServiceError):
    pass

class PlayerNotInGameError(GameServiceError):
    pass

class SecretNotFoundError(GameServiceError):
    pass

class badRequestError(GameServiceError):
    pass

class SetNotFoundError(GameServiceError):
    pass