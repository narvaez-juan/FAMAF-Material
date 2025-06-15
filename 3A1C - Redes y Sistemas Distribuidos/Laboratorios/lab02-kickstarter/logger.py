import logging


class Logger():
    """
    Logger se encarga de filtrar los mensajes según el nivel de detalle
    que se requiera en la ejecución. Según su llamado se obtendrá los
    siguientes mensajes:

    ERROR (log_error)

    WARNING (ERROR + log_warning)

    INFO (WARNING + log_info)

    DEBUG (INFO + log_debug)
    """

    _logger = logging.getLogger()

    def __init__(self):
        formatter = logging.Formatter(
            "%(name)s - %(levelname)s - "
            "%(filename)s:%(funcName)s - %(message)s"
        )
        logging.StreamHandler().setFormatter(formatter)

    def log_error(self, msg: str):
        """
        Log Error debe ser utiliazdo para eventos que detienen la ejecución o
        no deberían ocurrir en una ejecución correcta.
        """
        self._logger.error(msg, exc_info=True)

    def log_warning(self, msg: str):
        """
        Log Warning debe ser utilizado para eventos que requieren
        ser tomados en cuenta, pero no detienen necesariamente la ejecución.
        """
        self._logger.warning(msg)

    def log_info(self, msg: str):
        """
        Log Info debe ser utilizado para información que puede ser omitida
        en el debugging. Pero da una idea general del estado de la ejecución.
        """
        self._logger.info(msg)

    def log_debug(self, msg: str):
        """
        Log Debug debe ser utilizado para información muy detallada
        de cada paso de la ejecución para llegar a un entendimiento
        de dónde ocurre el error.
        """
        self._logger.debug(msg)
