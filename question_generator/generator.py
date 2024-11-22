from langchain import OpenAI, LLMChain
from langchain.prompts import PromptTemplate


class QuestionGenerator:
    def __init__(self):
        self.llm = OpenAI(temperature=0.7)
        self.template = PromptTemplate(
            input_variables=["book_title", "book_summary"],
            template="Generate a thought-provoking question about the book titled '{book_title}' which is about {book_summary}."
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.template)

    def generate_question(self, book):
        book_title = book['title']
        book_summary = book['summary']
        question = self.chain.run(book_title=book_title, book_summary=book_summary)
        return question

    def generate_multiple_questions(self, book, n=3):
        return [self.generate_question(book) for _ in range(n)]
