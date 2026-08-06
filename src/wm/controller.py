import win32con
import win32gui


class WindowController:
    def minimize(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def maximize(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def fullscreen(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SHOW_FULLSCREEN)

    def set_focus(self, hwnd: int):
        win32gui.SetForegroundWindow(hwnd)
