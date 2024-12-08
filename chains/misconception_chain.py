from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

class MisconceptionDetectionChain:
    def __init__(self, llm):
        self.llm = llm
        self.misconception_prompt = PromptTemplate(
            input_variables=["subject", "topic", "student_response", "key_points"],
            template="""
            Analyze the student's response for potential misconceptions:
            
            Subject: {subject}
            Topic: {topic}
            Key Points: {key_points}
            Student Response: {student_response}
            
            Identify:
            1. Common misconceptions present in the response
            2. Incorrect connections or assumptions
            3. Gaps in fundamental understanding
            4. Source of each misconception
            
            Format response as structured analysis with specific examples from the response.
            """
        )
        self.chain = RunnableSequence(
            first=self.misconception_prompt,
            last=self.llm
        ) 