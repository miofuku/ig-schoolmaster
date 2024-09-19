from models import db, Book


class UniversalBookRepository:
    def __init__(self):
        pass  # No need to load books from JSON file anymore

    def get_random_books(self, n):
        return [book.to_dict() for book in Book.query.order_by(db.func.random()).limit(n).all()]

    def search_books(self, query):
        return [book.to_dict() for book in Book.query.filter(
            (Book.title.ilike(f'%{query}%')) | (Book.author.ilike(f'%{query}%'))
        ).all()]

    def get_book_by_id(self, book_id):
        book = Book.query.get(book_id)
        return book.to_dict() if book else None

    def get_book_by_title(self, title):
        book = Book.query.filter(Book.title.ilike(f'%{title}%')).first()
        return book.to_dict() if book else None
