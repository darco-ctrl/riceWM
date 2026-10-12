from pathlib import Path

import app.paths as rice_paths

class LogFiles:
    LATEST = "rice_wm.log"
    PREVIOUS = "rice_wm.log.1"
    ARCHIVED = "rice_wm.log.2"

class EventLogger:
    def __init__(self):

        self._check_log_file()

        self.log_file: Path = Path()

    # checks file size and creates a new file if file is over 5 mb
    # deletes oldest log file when creating new one
    # only 3 file exists at a time log.txt, log_1, log_2
    # log.txt: latest, log_1: previous log, log_2: archived log
    def _check_log_file(self):
        log_file = rice_paths.log_folder / LogFiles.LATEST

        if not log_file.exists():
            log_file.touch()

        file_size = self._get_file_size(log_file)
        if file_size > 5:
            pass

    def _create_new_file(self):
        latest_log = rice_paths.log_folder / LogFiles.LATEST
        previous_log = rice_paths.log_folder / LogFiles.PREVIOUS
        archived_log = rice_paths.log_folder / LogFiles.ARCHIVED

        if archived_log.exists():
            archived_log.unlink()

        if previous_log.exists():
            archived_log = previous_log.with_name(LogFiles.ARCHIVED)
            previous_log.rename(archived_log)

        if latest_log.exists():
            previous_log = latest_log.with_name(LogFiles.PREVIOUS)
            latest_log.rename(previous_log)

            latest_log = rice_paths.log_folder / LogFiles.LATEST
            latest_log.touch()
        
        

    def _get_file_size(self, path: Path) -> float:
        return path.stat().st_size / 1024**2
