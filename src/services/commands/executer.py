

import src.app.paths as rice_paths
from src.core.data_manager import DataManager
from src.core.events.event_bus import eventBus
from src.services.commands.helper import CommandHelper


class CommandExecuter():
    def __init__(self, data_manager: DataManager):
        self.data_manager: DataManager = data_manager
        self.helper: CommandHelper = CommandHelper()
    
    def restart_application(self):
        eventBus.requestRestartApplication.emit()

    def open_theme(self):
        path = self.data_manager.get_current_theme_path()

        self.helper.open_file(path)

    def open_config(self): 
        path = self.data_manager.get_current_config_path()
        self.helper.open_file(path)

    def open_keymap(self):
        path = self.data_manager.get_keymap_path()
        self.helper.open_file(path)

    def open_app_config(self):
        path = self.data_manager.app_config.get_app_config_path()
        self.helper.open_file(path)

    def quit_app(self):
        eventBus.requestQuitApplication.emit()
