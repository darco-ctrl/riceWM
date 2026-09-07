import sys
from ctypes import windll

from src.app.app import App

MUTEX_NAME = "SeedMachine.RiceWM.Application"

def ensure_single_instance() -> bool:
    mutex = windll.kernel32.CreateMutexW(
        None,
        False,
        MUTEX_NAME
    )

    if not mutex:
        return False

    ERROR_ALREADY_EXISTS = 183

    if windll.kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
        return False

    global _mutex_handle
    _mutex_handle = mutex

    return True

if __name__ == "__main__":
    if not ensure_single_instance():
        sys.exit(0)
    
    App().run()
