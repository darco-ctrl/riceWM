from collections.abc import Callable

from app.event_logger import EventLogger, LogEventType
from src.core.data_manager import DataManager
from src.services.commands.executer import CommandExecuter


class CommandService: 
    def __init__(
        self, 
        logger: EventLogger, 
        data_manager: DataManager
    ):
        self.logger = logger
        self.executer: CommandExecuter = CommandExecuter(
            data_manager=data_manager
        )

        self.commands: dict[str, Callable] = (
            self.create_commands_dictionary()
        )

    def execute(self, command: str):
        if not command in self.commands:
            return

        self._log(command)
        self.commands[command]()

    def is_command(self, command: str) -> bool:
        return command in self.commands

    def create_commands_dictionary(self):
        commands: dict[str, Callable] = {
            ":restart": self.executer.restart_application,
            ":open-theme": self.executer.open_theme,
            ":open-config": self.executer.open_config,
            ":open-app-config": self.executer.open_app_config,
            ":open-keymap": self.executer.open_keymap,
            ":quit": self.executer.quit_app
        }

        return commands

    def _log(self, message: str):
        self.logger.log(
            log_type=LogEventType.EXECUTE_COMMAND,
            message=message
        )
