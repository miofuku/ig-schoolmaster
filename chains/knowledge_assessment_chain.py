from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

class KnowledgeAssessmentChain:
    def __init__(self, llm):
        self.llm = llm
        self.assessment_prompt = PromptTemplate(
            input_variables=["knowledge_area", "difficulty", "optional_material", "assessment_type"],
            template="""
            Generate a {assessment_type} assessment for {knowledge_area} at {difficulty} level.
            
            Context Material: {optional_material}
            
            Create an assessment that:
            1. Tests key concepts and understanding
            2. Includes a mix of question types
            3. Focuses on practical application
            4. Provides clear evaluation criteria
            
            Assessment:
            """
        )
        self.chain = RunnableSequence(
            first=self.assessment_prompt,
            last=self.llm
        )
    
    async def arun(self, inputs):
        return await self.chain.ainvoke(inputs) 