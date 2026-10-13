import logging
from logging.handlers import RotatingFileHandler

import app.paths as rice_paths


class LogEventType:
    KEY_PRESSED = "KEY_PRESSED"
    APPLICATION_START = "APPLICATION_START"
    APPLICATION_QUIT = "APPLICATION_QUIT"
    APPLICATION_RESTART = "APPLICATION_RESTART"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    LOAD_DATA = "LOAD_DATA"
    EXECUTE_COMMAND = "EXECUTE_COMMAND"
    

class RiceWMFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        return f"{timestamp}: {record.getMessage()}."


class EventLogger:
    def __init__(self):
        self.file_handler = self._get_file_handler()
        self.console_handler = self._get_console_handler()
        self.logger = self._get_logger()

        self.log(log_type=LogEventType.KEY_PRESSED, message="hello world")

    def _get_file_handler(self) -> RotatingFileHandler:
        path = rice_paths.log_folder / "rice_wm.log"
        
        handler = RotatingFileHandler(
            path,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        handler.setFormatter(RiceWMFormatter())
        return handler

    def _get_console_handler(self) -> logging.StreamHandler:
        handler = logging.StreamHandler()
        handler.setFormatter(RiceWMFormatter())
        return handler

    def _get_logger(self) -> logging.Logger: 
        logger = logging.getLogger("rice_wm")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        
        if not logger.handlers:
            logger.addHandler(self._get_file_handler())
            logger.addHandler(self._get_console_handler())

        return logger

    def log(self, message: str, log_type: str = LogEventType.INFO):
        log = f"[EVENT_TYPE: {log_type}]: {message}"

        self.logger.info(log)
