import random


class UniversalBookRepository:
    def __init__(self):
        self.books = [
            {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
            {"id": 2, "title": "1984", "author": "George Orwell"},
            {"id": 3, "title": "Pride and Prejudice", "author": "Jane Austen"},
            # Add more books...
        ]

    def get_random_books(self, n):
        return random.sample(self.books, min(n, len(self.books)))
