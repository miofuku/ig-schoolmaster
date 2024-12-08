from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

class ConceptVerificationChain:
    def __init__(self, llm):
        self.llm = llm
        self.verification_prompt = PromptTemplate(
            input_variables=["concept", "response"],
            template="""
            Evaluate the understanding of the following concept:
            
            Concept: {concept}
            Student's Response: {response}
            
            Provide:
            1. Accuracy assessment
            2. Missing key points
            3. Suggestions for improvement
            
            Evaluation:
            """
        )
        self.chain = RunnableSequence(
            first=self.verification_prompt,
            last=self.llm
        )
    
    async def arun(self, inputs):
        return await self.chain.ainvoke(inputs) 