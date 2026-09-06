

import os


class CommandHelper:
    def open_file(self, path: str):
        if not os.path.exists(path=path):
            return
        
        os.startfile(path)
