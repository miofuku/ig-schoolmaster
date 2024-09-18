import random
import json
from pathlib import Path


class UniversalBookRepository:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self):
        books_file = Path(__file__).parent / 'books.json'
        with open(books_file, 'r') as f:
            return json.load(f)

    def get_random_books(self, n):
        return random.sample(self.books, min(n, len(self.books)))

    def search_books(self, query):
        return [book for book in self.books if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]

    def get_book_by_id(self, book_id):
        try:
            book_id = int(book_id)
        except ValueError:
            return None
        return next((book for book in self.books if book['id'] == book_id), None)

    def get_book_by_title(self, title):
        return next((book for book in self.books if book['title'].lower() == title.lower()), None)