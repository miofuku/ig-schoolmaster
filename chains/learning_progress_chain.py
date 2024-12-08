from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

class LearningProgressChain:
    def __init__(self, llm):
        self.llm = llm
        self.progress_prompt = PromptTemplate(
            input_variables=["topic", "standards", "history", "current_assessment"],
            template="""
            Given the following information:
            
            Topic: {topic}
            Curriculum Standards: {standards}
            Learning History: {history}
            Current Assessment: {current_assessment}
            
            Analyze:
            1. Which learning objectives have been mastered
            2. Which concepts need reinforcement
            3. What should be the next learning focus
            4. Recommended learning activities
            
            Format as structured recommendations with clear next steps.
            """
        )
        self.chain = RunnableSequence(
            first=self.progress_prompt,
            last=self.llm
        )
    
    async def arun(self, inputs):
        return await self.chain.ainvoke(inputs) 