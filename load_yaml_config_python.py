import yaml
# Load the configuration file
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
# Create a set of books
books = set()
for book_config in config['books']:
    name = book_config['name']
    description = book_config['description']
    pages = book_config['pages']
    genre = book_config['genre']
    book = {'name': name, 'description': description, 'pages': pages, 'genre': genre}
    books.add(book)
