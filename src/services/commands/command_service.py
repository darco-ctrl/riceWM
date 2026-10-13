from collections.abc import Callable

from app.event_logger import EventLogger, LogEventType
from src.core.data_manager import DataManager
from src.services.commands.executer import CommandExecuter


class CommandService:
    """Manages application commands and their execution."""
    
    def __init__(
        self, 
        logger: EventLogger, 
        data_manager: DataManager
    ):
        self._logger = logger
        self._executer: CommandExecuter = CommandExecuter(
            data_manager=data_manager
        )

        self._commands: dict[str, Callable] = (
            self._create_commands_dictionary()
        )
        

    def _create_commands_dictionary(self):
        commands: dict[str, Callable] = {
            ":restart": self._executer.restart_application,
            ":open-theme": self._executer.open_theme,
            ":open-config": self._executer.open_config,
            ":open-app-config": self._executer.open_app_config,
            ":open-keymap": self._executer.open_keymap,
            ":quit": self._executer.quit_app
        }

        return commands


    def _log(self, message: str):
        self._logger.log(
            log_type=LogEventType.EXECUTE_COMMAND,
            message=message
        )


    def execute(self, command: str):
        if not command in self._commands:
            return

        self._log(command)
        self._commands[command]()


    def is_command(self, command: str) -> bool:
        return command in self._commands
