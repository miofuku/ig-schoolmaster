from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from config import OPENAI_API_KEY


class QuestionGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY,
            model_name="gpt-3.5-turbo"
        )
        self.prompt = ChatPromptTemplate.from_template(
            "Generate a thought-provoking question about the book titled '{book_title}' "
            "which is about {book_summary}. The question should encourage critical thinking."
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def generate_question(self, book):
        return self.chain.run(
            book_title=book['title'],
            book_summary=book['summary']
        ).strip()

    def generate_multiple_questions(self, book, n=3):
        return [self.generate_question(book) for _ in range(n)]
