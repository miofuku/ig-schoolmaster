from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class KnowledgeGapChain(LLMChain):
    def __init__(self, llm):
        prompt = PromptTemplate(
            input_variables=["assessment_history", "target_competencies"],
            template="""
            Analyze the student's assessment history and identify knowledge gaps:
            
            Assessment History: {assessment_history}
            Target Competencies: {target_competencies}
            
            Provide:
            1. Identified knowledge gaps
            2. Critical areas needing attention
            3. Recommended focus areas
            """
        )
        super().__init__(llm=llm, prompt=prompt) 