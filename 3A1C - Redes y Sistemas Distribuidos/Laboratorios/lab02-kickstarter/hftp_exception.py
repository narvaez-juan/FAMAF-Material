import constants

from logger import Logger

logger = Logger()


class HFTPException(Exception):
    """
    Manejador de excepciones y errores de nuestro protocolo HFTP.
    """

    def __init__(
            self,
            error_code: int,
            error_msg: str,
            error_name="HFTP Exception"):
        self.error_code = error_code
        """
        Código de error
        """
        self.error_msg = error_msg
        """
        Mensaje de error
        """
        self.error_name = error_name
        """
        Nombre del error o excepción asociado
        """
        logger.log_warning(f"HFTPException: {self}")

    def __str__(self):
        return f"[{self.error_code}] {self.error_name}: {self.error_msg}"


class MalformedParserException(HFTPException):
    """
    Malformed Parser Exception.

    Excepciones malformadas del Parser.

    Explicación detallada: se encontró un carácter \\n
    fuera de un terminador de pedido \\r\\n.
    """

    def __init__(self):
        super().__init__(
            constants.BAD_EOL,
            "found \\n without \\r",
            constants.PARSER_STATUS_MALFORMED
        )


class UnknownParserException(HFTPException):
    """
    Unknown Parser Exception.

    Excepciones desconocidas del Parser.

    Explicación detallada: alguna malformación del pedido impidió procesarlo.
    """

    def __init__(self):
        super().__init__(
            constants.BAD_REQUEST,
            "Request was no accepted",
            constants.UnknownParserException
        )


class InternalErrorException(HFTPException):
    """
    Internal Error Exception.

    Excepciones internal del servidor.

    Explicación detallada: el servidor tuvo algún fallo
    interno al intentar procesar el pedido.
    """

    def __init__(self, exception: str):
        super().__init__(
            constants.INTERNAL_ERROR,
            str(exception),
            constants.error_messages[constants.INTERNAL_ERROR]
        )


class InvalidCommandException(HFTPException):
    """
    Invalid Command Exception.

    Cuando la cantidad de argumentos es inválido.

    Explicación detallada: el comando no está en
    la lista de comandos aceptados.
    """

    def __init__(self):
        super().__init__(
            constants.INVALID_COMMAND,
            "Invalid Command",
            constants.error_messages[constants.INVALID_COMMAND]
        )


class InvalidArgumentsException(HFTPException):
    """
    Invalid Arguments Exception.

    Cuando la cantidad de argumentos es inválido.
    """

    def __init__(self):
        super().__init__(
            constants.INVALID_ARGUMENTS,
            "Invalid Arguments for current command",
            constants.error_messages[constants.INVALID_ARGUMENTS]
        )


class FileNotFoundException(HFTPException):
    """
    File Not Found Exception.

    Cuando se pide un archivo que no se encuentra en el directorio servido.

    Explicación detallada: el pedido se refiere a un archivo inexistente.
    """

    def __init__(self):
        super().__init__(
            constants.FILE_NOT_FOUND,
            "File not found on the Server permitted directory",
            constants.error_messages[constants.FILE_NOT_FOUND]
        )


class BadOffsetException(HFTPException):
    """
    Invalid Offset for command.

    Cuando el offset de `get_slice` es inválido.

    Explicación detallada: el pedido se refiere
    a una posición inexistente en un archivo.
    """

    def __init__(self):
        super().__init__(
            constants.BAD_OFFSET,
            "Amount of bytes out of bounds",
            constants.error_messages[constants.BAD_OFFSET]
        )


class InvalidCommandSizeException(HFTPException):
    def __init__(self):
        super().__init__(
            constants.FILE_NOT_FOUND,
            "Amount of bytes out of bounds",
            constants.error_messages[constants.FILE_NOT_FOUND]
        )
