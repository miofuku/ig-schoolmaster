from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

class KnowledgeAssessmentChain:
    def __init__(self, llm):
        self.llm = llm
        self.assessment_prompt = PromptTemplate(
            input_variables=["knowledge_area", "difficulty", "optional_material", "assessment_type"],
            template="""
            Generate a {difficulty}-level assessment for {knowledge_area}.
            Type: {assessment_type}
            Additional Material: {optional_material}
            
            Structure the assessment with:
            1. Multiple Choice Questions (3-4 questions)
            2. True/False Questions (2-3 statements)
            3. Short Answer Questions (1-2 questions)
            4. Practical Application Task
            
            Include clear evaluation criteria at the end.
            Format the response in a clean, readable way.
            """
        )
        self.chain = RunnableSequence(
            first=self.assessment_prompt,
            last=self.llm
        )
    
    async def arun(self, inputs):
        result = await self.chain.ainvoke(inputs)
        # Ensure we return just the content string
        return result.content if hasattr(result, 'content') else str(result) 