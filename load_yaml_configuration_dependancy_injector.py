from dependency_injector import containers, providers
class Book:
    def __init__(self, name, description, authors, pages):
        self.name = name
        self.description = description
        self.authors = authors
        self.pages = pages
class BookContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    book_provider = providers.Factory(
        Book,
        name=config.books[0]['name'],
        description=config.books[0]['description'],
        authors=config.books[0]['authors'],
        pages=config.books[0]['pages']
    )
if __name__ == '__main__':
    with open("books.yaml", "r") as f:
        books_data = yaml.safe_load(f)
    container = BookContainer(config={'books': books_data})
    book = container.book_provider()
    print(book.name)
    print(book.description)
    print(book.authors)
    print(book.pages)
