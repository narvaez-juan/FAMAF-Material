#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import sys
import signal
import socket
import logging
import optparse
import threading
from logger import Logger
from connection import Connection
from constants import DEFAULT_ADDR, DEFAULT_PORT, DEFAULT_DIR


logger = Logger()


class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    MAX_AMOUNT_CLIENTS = 1
    """
    Maxima cantidad de clientes que pueden conectarse en simultaneo.
    """

    def __init__(
            self,
            addr=DEFAULT_ADDR,
            port=DEFAULT_PORT,
            directory=DEFAULT_DIR):
        print("Serving %s on %s:%s." % (directory, addr, port))

        self.directory = directory

        # Crea el socket TCP (IPv4)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Permite reutilizar la dirección en caso de reiniciar el servidor.
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Asocia el socket a la dirección y puerto indicados.
        self.socket.bind((addr, port))

        # Pone el socket en modo escucha, preparado para aceptar conexiones.
        self.socket.listen(self.MAX_AMOUNT_CLIENTS)

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez
        y se espera a que concluya antes de seguir.
        """
        while True:
            # Espera a que un cliente se conecte.
            # accept() devuelve (socket, address) del cliente.
            # Usamos client_socket para comunicarnos con el cliente.
            socket, address = self.socket.accept()
            # se crea un hilo para manejar la conexión con el cliente
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(socket, address))
            # se marca el hilo como daemon para que se cierre
            # automaticamente cuando el hilo principal termine
            # de ejecutarse.
            client_thread.daemon = True
            # se inicia el hilo
            client_thread.start()

    # maneja la conexión con un cliente
    def handle_client(self, client_socket, address):
        """
        Maneja la conexión con un cliente.
        """
        try:
            connection = Connection(client_socket, address, self.directory)
            connection.handle()
        except Exception as e:
            socket.close()
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
            print(f"Closing connection from {address}")


def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)
    parser.add_option(
        "-v", "--verbose",
        dest="level",
        action="store",
        help="Determina cuanta información de depuración mostrar"
        "(valores posibles son: ERROR, WARN, INFO, DEBUG)",
        default="ERROR"
    )

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    try:
        server = Server(options.address, port, options.datadir)

        def handle_sigterm(signalNumber, frame):
            logger.log_warning(f"Received SIGTERM. Closing Sockets")
            server.close()
            sys.exit()

        signal.signal(signal.SIGTERM, handle_sigterm)

        server.serve()
    except KeyboardInterrupt as keyboardInterrupt:
        server.close()
        raise keyboardInterrupt


def setup_logger(level):
    DEBUG_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN': logging.WARNING,
        'ERROR': logging.ERROR,
    }

    # Setar verbosidad
    code_level = DEBUG_LEVELS.get(level)  # convertir el str en codigo
    logging.basicConfig(format='[%(levelname)s] - %(message)s')
    logger = Logger()
    logger._logger.setLevel(code_level)


if __name__ == '__main__':
    main()
