from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class ConceptVerificationChain(LLMChain):
    def __init__(self, llm):
        prompt = PromptTemplate(
            input_variables=["student_response", "concept"],
            template="""
            Evaluate the student's understanding of {concept} based on their response:
            
            Student Response: {student_response}
            
            Provide an analysis covering:
            1. Accuracy of understanding
            2. Identification of misconceptions
            3. Suggestions for improvement
            """
        )
        super().__init__(llm=llm, prompt=prompt) 