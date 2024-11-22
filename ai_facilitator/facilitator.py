from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from collections import defaultdict
import random
from config import OPENAI_API_KEY
from knowledge_map.mapper import KnowledgeMapper


class AIFacilitator:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY,
            model_name="gpt-3.5-turbo"
        )
        self.context_prompts = defaultdict(list)
        self.initialize_context_prompts()
        self.knowledge_mapper = KnowledgeMapper()

    def initialize_context_prompts(self):
        self.context_prompts['reading'] = [
            "How does the text challenge or reinforce your existing beliefs?",
            "What connections can you draw between this reading and your personal experiences?",
            "If you could ask the author one question, what would it be and why?",
            "How might this text be interpreted differently in various cultural contexts?",
            "What aspects of the reading did you find most thought-provoking or surprising?"
        ]
        self.context_prompts['discussion'] = [
            "How have your peers' perspectives influenced your understanding of the topic?",
            "What new questions have emerged for you during this discussion?",
            "How might you apply the insights from this discussion to real-world situations?",
            "What aspects of the discussion challenged your initial thoughts on the subject?",
            "How would you synthesize the different viewpoints presented in this conversation?"
        ]

    def generate_prompt(self, context, user_data=None):
        context_specific_prompts = self.context_prompts.get(context, [])
        selected_prompt = random.choice(context_specific_prompts) if context_specific_prompts else f"What aspects of {context} do you find most intriguing?"
        return selected_prompt

    def generate_explore_questions(self, book):
        if not isinstance(book, dict) or 'title' not in book or 'author' not in book:
            raise ValueError("Invalid book data provided")

        # Generate questions based on the knowledge base
        return self.knowledge_mapper.generate_questions_from_knowledge(book['title'])

    def generate_reflection_prompt(self, topic):
        prompt = ChatPromptTemplate.from_template(
            "Generate a reflective question about {topic} that encourages deep personal insight and critical thinking."
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(topic=topic).strip()

