from typing import Callable

from src.core.data_manager import DataManager
from src.core.events.event_bus import eventBus
from src.services.commands.executer import CommandExecuter


class CommandService: 
    def __init__(self, data_manager: DataManager):
        self.executer: CommandExecuter = CommandExecuter(
            data_manager=data_manager
        )

        self.commands: dict[str, Callable] = (
            self.create_commands_dictionary()
        )

    def execute(self, command: str):
        if not command in self.commands:
            return

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
