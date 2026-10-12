import logging
from logging.handlers import RotatingFileHandler

import app.paths as rice_paths

class LogType:
    KEY_PRESS = "KEY_PRESS"

class RiceWMFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        log = f"{timestamp}: {record.getMessage()}."
        
        return log


class EventLogger:
    def __init__(self):
        self.handler = self._get_handler()
        self.logger = self._get_logger()

        self.log(log_type=LogType.KEY_PRESS, message="hello world")

    def _get_handler(self) -> RotatingFileHandler:
        path = rice_paths.log_folder / "rice_wm.log"
        
        handler = RotatingFileHandler(
            path,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        handler.setFormatter(RiceWMFormatter())
        return handler

    def _get_logger(self) -> logging.Logger: 
        logger = logging.getLogger("rice_wm")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.handler)

        return logger

    def log(self, log_type: str, message: str):
        log = f"[TYPE: {log_type}]: {message}"

        self.logger.info(log)
