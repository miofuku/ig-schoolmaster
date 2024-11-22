import random
from collections import defaultdict
from langchain import OpenAI, LLMChain
from langchain.prompts import PromptTemplate


class AIFacilitator:
    def __init__(self):
        self.llm = OpenAI(temperature=0.7)
        self.context_prompts = defaultdict(list)
        self.initialize_context_prompts()

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

        rule_based_prompt = random.choice([
            f"How does the theme of '{book['title']}' relate to contemporary issues?",
            f"What questions would you ask the author of '{book['title']}' if you had the chance?",
            f"How might the ideas in '{book['title']}' challenge your existing beliefs?",
            f"What connections can you draw between '{book['title']}' and other books you've read?",
            f"How could the concepts in '{book['title']}' be applied to solve real-world problems?"
        ])
        
        lm_prompt = self.generate_lm_prompt(f"the book '{book['title']}' by {book['author']}")
        return f"{rule_based_prompt} Additionally, {lm_prompt}"

    def generate_lm_prompt(self, context):
        template = PromptTemplate(
            input_variables=["context"],
            template="Generate a thought-provoking question about {context}:"
        )
        chain = LLMChain(llm=self.llm, prompt=template)
        return chain.run(context=context)

