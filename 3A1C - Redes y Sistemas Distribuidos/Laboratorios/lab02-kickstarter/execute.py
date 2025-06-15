import os
import base64
import constants as const

from logger import Logger
from command import Command
from hftp_exception import (
    BadOffsetException,
    FileNotFoundException,
    InvalidArgumentsException,
    InvalidCommandException
)


logger = Logger()


class Execute():
    """
    Manejador de comandos.
    """

    def __init__(self, command: Command, base_dir: str):
        logger.log_debug(
            f"Creating Handler Object with command: {command} "
            f"and base_dir: {base_dir}"
        )
        self.command: Command = command
        """
        Comandos
        """
        self.status = const.EXECUTE_STATUS_OK
        """
        Estado de la ejecución del comando
        """
        self.base_dir = base_dir
        """
        Directorio
        """
        self.err_msg = const.CODE_OK
        """
        Estado de código / Mensajes de error
        """

    def execute(self):
        """
        Ejecuta un comando válido.

        Si recibe un comando inválido levanta una excepción y finaliza.
        """
        logger.log_info(f"Executing command: {self.command.name} "
                        f"{' '.join(self.command.arguments)}")

        # Corroboramos si el comando es válido
        if (self.command.name == self.command.COMMAND_GET_FILE_LISTING):
            return self.execute_get_file_listing()
        elif (self.command.name == self.command.COMMAND_GET_METADATA):
            return self.execute_get_metadata()
        elif (self.command.name == self.command.COMMAND_GET_SLICE):
            return self.execute_get_slice()
        elif (self.command.name == self.command.COMMAND_QUIT):
            return self.execute_quit()
        elif (self.command.name == ''):
            return (const.CODE_OK, list())
        else:
            # No encontró ningún comando válido...
            logger.log_debug("Could not find handler function for "
                             f"'{self.command.name}' command")

            self.status = const.EXECUTE_INVALID_COMMAND
            self.err_msg = const.INVALID_COMMAND

            logger.log_debug(f"Status: {self.status}")
            raise InvalidCommandException()

    def execute_get_file_listing(self):
        """
        Ejecuta el comando `get_file_listing`
        """
        logger.log_debug("Executing execute_get_file_listing")

        if (len(self.command.arguments) == 0):
            try:
                directory = os.listdir(self.base_dir)
            except FileNotFoundError:
                self.status = const.FILE_NOT_FOUND
                self.err_msg = const.FILE_NOT_FOUND
                return (self.err_msg, list())
        else:
            self.status = const.EXECUTE_INVALID_ARGUMENTS
            self.err_msg = const.INVALID_ARGUMENTS
            raise InvalidArgumentsException()
        return (self.err_msg, directory)

    def execute_get_metadata(self):
        """
        Ejecuta el comando `get_metadata`.

        Maneja excepciones.
        """
        logger.log_debug("Executing execute_get_metadata")

        if (len(self.command.arguments) == 1):
            # Obtener el path correspondiente
            try:
                path = f"{self.base_dir}/{self.command.arguments[0]}"
                logger.log_debug(f"getting metadata of file '{path}'")

                # Obtener el tamaño del archivo
                size = os.path.getsize(path)
                logger.log_debug(f"size of {path}: {size}")
            except (FileNotFoundError, OSError):
                self.status = const.FILE_NOT_FOUND
                self.err_msg = const.FILE_NOT_FOUND
                raise FileNotFoundException()
        else:
            self.status = const.EXECUTE_INVALID_ARGUMENTS
            self.err_msg = const.INVALID_ARGUMENTS
            raise InvalidArgumentsException()

        return_list = list()
        return_list.append(str(size))

        # Retorna una lista
        return (self.err_msg, return_list)

    def execute_get_slice(self):
        """
        Ejecuta el comando `get_slice`.

        Maneja excepciones.
        """
        logger.log_debug("Executing execute_get_slice")

        if (len(self.command.arguments) == 3):
            path = f"{self.base_dir}/{self.command.arguments[0]}"
            file_size = os.path.getsize(path)
            try:
                offset = int(self.command.arguments[1])
                slice_size = int(self.command.arguments[2])
                request_size = offset + slice_size
            except ValueError:
                raise InvalidArgumentsException()

            if (file_size >= request_size):
                try:
                    # No es necesario llamar a close ya que
                    # el 'with' lo hace automáticamente
                    # rb -> read bytes
                    with open(path, "rb") as file:
                        # Se mueve al punto dónde tiene que empezar a leer
                        file.seek(offset)
                        encoded_read = file.read(slice_size)
                        logger.log_debug(
                            "encoded_read (of size "
                            f"{request_size}): {encoded_read}")

                    # Se encodea en base64 para que entre en tipo ASCII
                    data = base64.b64encode(encoded_read).decode('ascii')
                    logger.log_debug(f"base64 encoded data: {data}")

                    return_list = list()
                    return_list.append(data)
                except (FileNotFoundError, OSError):
                    self.status = const.FILE_NOT_FOUND
                    self.err_msg = const.error_messages[const.FILE_NOT_FOUND]
                    raise FileNotFoundException()
            else:
                self.status = const.BAD_OFFSET
                self.err_msg = const.EXECUTE_INVALID_COMMAND
                raise BadOffsetException()
        else:
            self.status = const.EXECUTE_INVALID_ARGUMENTS
            self.err_msg = const.INVALID_ARGUMENTS
            raise InvalidArgumentsException()

        return (self.err_msg, return_list)

    def execute_quit(self):
        """
        Ejecuta el comando `quit`
        """
        logger.log_debug(f"Executing execute_quit")

        if (len(self.command.arguments) != 0):
            raise InvalidArgumentsException()

        self.status = const.EXECUTE_STATUS_EXIT
        return (const.CODE_OK, list())
