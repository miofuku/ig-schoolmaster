from models import db, Book
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from config import OPENAI_API_KEY


class UniversalBookRepository:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY,
            model_name="gpt-3.5-turbo"
        )

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

    def generate_book_summary(self, book):
        template = PromptTemplate(
            input_variables=["title", "author", "summary"],
            template="Summarize the book '{title}' by {author}: {summary}"
        )
        chain = LLMChain(llm=self.llm, prompt=template)
        return chain.run(title=book['title'], author=book['author'], summary=book['summary'])
