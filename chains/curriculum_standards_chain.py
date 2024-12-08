from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

class CurriculumStandardsChain:
    def __init__(self, llm):
        self.llm = llm
        self.standards_prompt = PromptTemplate(
            input_variables=["subject", "grade", "topic"],
            template="""
            For {subject} at grade {grade}, focusing on {topic}:
            
            1. List the core learning objectives that should be mastered
            2. Identify prerequisite knowledge required
            3. Specify key concepts and skills to be developed
            4. Define measurable learning outcomes
            
            Format the response as a structured JSON with:
            - prerequisites: [list of required prior knowledge]
            - core_concepts: [list of main concepts]
            - learning_objectives: [list of specific objectives]
            - skills: [list of skills to develop]
            - assessment_criteria: [list of measurable outcomes]
            """
        )
        self.chain = RunnableSequence(
            first=self.standards_prompt,
            last=self.llm
        )
    
    async def arun(self, inputs):
        return await self.chain.ainvoke(inputs) 