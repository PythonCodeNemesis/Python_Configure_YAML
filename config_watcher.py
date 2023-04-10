import yaml
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dependency_injector import containers, providers
class Book:
    def __init__(self, name, description, authors, pages, version):
        self.name = name
        self.description = description
        self.authors = authors
        self.pages = pages
        self.version = version
class BookContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    book_provider = providers.Factory(
        Book,
        name=config.books[0]['name'],
        description=config.books[0]['description'],
        authors=config.books[0]['authors'],
        pages=config.books[0]['pages'],
        version=config.version
    )
def load_config():
    with open("books.yaml", "r") as f:
        books_data = yaml.safe_load(f)
        version = books_data.pop("version", None)
        return (books_data, version)
def update_config():
    config, version = load_config()
    container = BookContainer(config={'books': config, 'version': version})
    return container
class ConfigEventHandler(FileSystemEventHandler):
    def __init__(self):
        self._observer = Observer()
        self._observer.schedule(self, ".", recursive=False)
    def on_modified(self, event):
        if event.src_path.endswith(".yaml"):
            print("Configuration file modified")
            container = update_config()
            # update all the book instances with new version
            for book in container.book_provider.all_objects:
                book.version = container.config.version
def start_config_watcher():
    event_handler = ConfigEventHandler()
    event_handler._observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        event_handler._observer.stop()
    event_handler._observer.join()
if __name__ == '__main__':
    container = update_config()
    for book in container.book_provider.all_objects:
        print(f"{book.name}: {book.version}")
    start_config_watcher()
