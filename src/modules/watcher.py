import logging
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from utils import process_siem_event_file


class Watcher:
    def __init__(self):
        self.observer = Observer()

    def run(self, event_handler, dir_to_watch):
        self.observer.schedule(event_handler, dir_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            logging.error("Error casb siem watcher get interrupted")

        self.observer.join()


class SiemHandler(FileSystemEventHandler):
    def __init__(self, configs):
        self.configs = configs

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == "created":
            logging.info("SiemHandler - Received created event - %s" % event.src_path)
            process_siem_event_file(self.configs, event.src_path)


def create_watcher_and_run(handler, monitored_dir):
    watcher = Watcher()
    watcher.run(handler, monitored_dir)


def create_siem_watcher_and_run(configs):
    create_watcher_and_run(SiemHandler(configs), configs.user_config_src_path)
