from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

class KnowledgeAssessmentChain:
    def __init__(self, llm):
        self.llm = llm
        self.assessment_prompt = PromptTemplate(
            input_variables=["knowledge_area", "difficulty", "key_points", "progress", "assessment_type"],
            template="""You are an expert assessment designer who creates engaging, thought-provoking assessments.

Design a {difficulty}-level assessment for {knowledge_area} that promotes deep understanding.

Context:
Key Learning Points: {key_points}
Current Progress: {progress}
Assessment Type: {assessment_type}

Create an assessment that:

1. Conceptual Understanding (40%):
- Multiple-choice questions that test understanding, not just recall
- Questions that address common misconceptions
- Scenarios that require application of concepts

2. Critical Thinking (30%):
- Open-ended questions that promote reasoning
- Problems that require connecting multiple concepts
- Real-world applications of knowledge

3. Communication Skills (30%):
- Opportunities to explain thinking
- Tasks requiring clear articulation of concepts
- Peer teaching/explanation scenarios

For each question:
- State the specific learning objective being assessed
- Provide clear evaluation criteria
- Include sample responses at different levels of understanding

Format the assessment to be engaging and encourage deep thinking rather than memorization.
Include metacognitive prompts that help students reflect on their understanding.
"""
        )
        self.chain = RunnableSequence(
            first=self.assessment_prompt,
            last=self.llm
        )
    
    async def arun(self, inputs):
        result = await self.chain.ainvoke(inputs)
        return result.content if hasattr(result, 'content') else str(result) 