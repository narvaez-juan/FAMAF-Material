# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

# import traceback
from constants import CODE_OK, INTERNAL_ERROR
from logger import Logger
from parser import Parser
from execute import Execute
from response_manager import ResponseManager
from hftp_exception import (
    HFTPException,
    InternalErrorException,
    MalformedParserException,
    UnknownParserException,
    InvalidArgumentsException,
    InvalidCommandSizeException
)


logger = Logger()


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """
    def __init__(self, socket, address, directory):
        logger.log_debug(
            f"Connection with socket {socket}"
            f" and directory: {directory} created."
        )

        self.socket = socket
        """
        Conexion socket.
        """
        self.current_directory = directory
        """
        Directorio actual.
        """
        self.connected = True
        """
        Sigue en conexion o no
        """
        self.address = address
        """
        Direccion IP y Puerto del cliente
        """

    def close_connection(self):
        """
        Cierra la conexion.
        """
        self.socket.close()
        logger.log_info(f"ENDING a connection with client...")

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        logger.log_info(f"STARTING a connection with client")

        try:
            while self.connected:

                parser = Parser(self.socket)

                response_manager = ResponseManager(self.socket)

                try:
                    command = parser.get_next_command()
                    logger.log_info(f"Command fetched from socket: {command}")

                except MalformedParserException as malformedException:
                    logger.log_info(f"{malformedException}")
                    response_manager.send_error(malformedException)
                    break

                except UnknownParserException as UnknownException:
                    logger.log_info(f"{UnknownException}")
                    response_manager.send_error(UnknownException)
                    break

                except InvalidCommandSizeException as invalidCommandSize:
                    response_manager.send_error(invalidCommandSize)
                    break

                try:
                    executer = Execute(command, self.current_directory)

                    response = executer.execute()

                    response_manager.send_response(response[0],
                                                   command, response[1])
                except HFTPException as hftpException:
                    response_manager.send_error(hftpException)

                self.connected = command.name != 'quit'
        except Exception as exception:
            logger.log_error(
                f"CODE ERROR: {INTERNAL_ERROR} - "
                f"Internal Error. Exception: {exception}"
            )
            # logger.log_debug(traceback.format_exc())
            response_manager.send_error(InternalErrorException(exception))

        self.close_connection()
