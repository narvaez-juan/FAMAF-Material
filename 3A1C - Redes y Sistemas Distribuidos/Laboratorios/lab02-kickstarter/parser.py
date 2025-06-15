import socket
import constants as const

from logger import Logger
from command import Command
from hftp_exception import (
    MalformedParserException,
    UnknownParserException,
    InvalidCommandSizeException
)

logger = Logger()


class Parser(object):
    """
    Parsea los mensajes obtenidos mediante la conexión por un socket.
    """
    PARSER_BUFFER_SIZE = 2 ** 12  # in bytes

    def __init__(self, socket: socket.socket):
        logger.log_debug("__init__ PARSER")

        self.buffer = list()
        """
        Buffer utilizado para leer bytes.
        """
        self.socket = socket
        """
        Conexión socket.
        """
        self.status = const.PARSER_STATUS_OK
        """
        Estado actual del parser.
        """

    def read_byte(self) -> chr:
        """
        Funcion para leer bytes
        """
        try:
            logger.log_debug(f"read_byte() buffer: {self.buffer}")

            # if(self.buffer.pop(0) == '\\x00') # NOTE Puede mejorar esto

            return chr(self.buffer.pop(0))
        except IndexError:
            # Si ya no tiene mas data, busca mas data del buffer
            self.buffer.extend(self.socket.recv(self.PARSER_BUFFER_SIZE))
            logger.log_debug(
                f"{len(self.buffer)} bytes fetched from socket."
                f" Current buffer: {self.buffer}"
            )
            return chr(self.buffer.pop(0))

    def flush_command(self):
        """
        Desecha el ingreso del socket hasta
        el inicio de un nuevo comando.

        Se utiliza para cuando el usuario ingresa
        comandos invalidos pero sigue enviando informacion.

        No cierra conexion.
        """
        while True:
            try:
                # Index del elemento '\r'
                chr_r_index = self.buffer.index(
                    const.PARSER_ASCII_CARRIAGE_RETURN)

                chr_n_index = chr_r_index + 1

                # Valida que el elemento el buffer sea '\n'
                if (self.buffer[chr_n_index] != const.PARSER_ASCII_LINE_FEED):
                    raise ValueError()
                else:
                    # Si lo es, limpia el buffer hasta ese elemento
                    self.buffer = self.buffer[chr_n_index + 1:]
                    break
            except ValueError:
                # Limpiamos el buffer completo
                self.buffer = list()
                # Si ya no tiene mas data, busca mas data del buffer
                self.buffer.extend(self.socket.recv(self.PARSER_BUFFER_SIZE))

    def get_next_command(self):
        """
        Obtiene y devuelve el comando de un socket.

        Los comandos deben finalizar en `\\r\\n`
        """
        logger.log_debug("Executing get_next_command()")

        command_str = ""
        tmp_str = ""
        malformed = False
        flush = False

        # Buscamos '\r\n'
        while True:
            if not flush and len(command_str) >= const.MAX_LENGTH_COMMAND:
                flush = True
                self.flush_command()
                break

            c_byte = self.read_byte()

            command_str += c_byte

            if command_str.endswith('\r\n'):
                # Esperamos hasta '\r\n'
                break
            elif c_byte != '\r' and tmp_str == '\n':
                malformed = True
                break
            tmp_str = c_byte

        if malformed:
            logger.log_warning("Malformed command. Raising exception")
            raise MalformedParserException()

        if flush:
            logger.log_warning("Invalid long size command. Raising exception")
            raise InvalidCommandSizeException()

        try:
            if (command_str[-2:-1] == "\r"):
                # Obtenemos las palabras
                command_str = command_str.lstrip('\x00')
                words = command_str.split(' ')
                logger.log_debug(f"command_str.split: {words}")

                # Eliminamos '\r\n\'
                words[-1] = words[-1].rstrip(const.EOL)
                logger.log_info(f"words: {words}")
            else:
                logger.log_warning("Malformed command. Raising exception")
                raise MalformedParserException()
        except Exception as e:
            logger.log_warning("Unexpected Parser Error. Raising exception")
            raise UnknownParserException()

        # Seteamos el comando
        # El primero es el comando
        # el segundo son los argumentos del comando
        command = Command(words[0], words[1:])
        return command
