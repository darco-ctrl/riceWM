from pynput import keyboard

from core.hotkey.event_bus import events


class HotKeyManager:
    def __init__(self) -> None:
        self.listner = keyboard.GlobalHotKeys({"<ctrl>+<alt>+<enter>": self.on_hotkey})

    def start(self):
        self.listner.start()

    def on_hotkey(self):
        print("Hot key pressed")
        events.helloRequested.emit()
