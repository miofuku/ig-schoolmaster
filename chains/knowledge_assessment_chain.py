from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class KnowledgeAssessmentChain(LLMChain):
    def __init__(self, llm):
        prompt = PromptTemplate(
            input_variables=["knowledge_area", "difficulty", "optional_material", "assessment_type"],
            template="""
            Generate an assessment for the following knowledge area:
            Knowledge Area: {knowledge_area}
            Difficulty Level: {difficulty}
            Additional Material Context: {optional_material}
            Assessment Type: {assessment_type}
            
            Consider:
            1. Core concepts in the specified area
            2. Real-world applications
            3. Common misconceptions
            4. Interdisciplinary connections
            
            Generate:
            1. Conceptual questions
            2. Application scenarios
            3. Critical thinking challenges
            4. Self-reflection prompts
            """
        )
        super().__init__(llm=llm, prompt=prompt) 