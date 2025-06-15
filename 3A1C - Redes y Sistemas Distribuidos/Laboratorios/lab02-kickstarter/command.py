class Command():
    """
    Comandos válidos en el protocolo.
    """
    COMMAND_GET_SLICE = 'get_slice'
    COMMAND_GET_METADATA = 'get_metadata'
    COMMAND_GET_FILE_LISTING = 'get_file_listing'
    COMMAND_QUIT = 'quit'

    def __init__(self, name: str, arguments: list):
        self.name = name
        self.arguments = arguments

    def __str__(self) -> str:
        return f"Command(name = {self.name}, arguments = {self.arguments})"
