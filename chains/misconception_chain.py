from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

class MisconceptionDetectionChain:
    def __init__(self, llm):
        self.llm = llm
        self.misconception_prompt = PromptTemplate(
            input_variables=["subject", "topic", "student_response", "key_points"],
            template="""You are an experienced {subject} educator who excels at identifying and addressing student misconceptions.

Analyze this student response with the following structured approach:

Topic: {topic}
Expected Key Points: {key_points}
Student Response: {student_response}

1. Knowledge Assessment:
- What core concepts has the student grasped correctly?
- What key points are missing or misunderstood?

2. Misconception Analysis:
- Identify specific misconceptions in the response
- Explain the likely source of each misconception
- Describe how each misconception might impact future learning

3. Conceptual Framework:
- How does the student's mental model differ from the accurate understanding?
- What foundational concepts need clarification?

4. Learning Path Recommendations:
- Suggest specific activities to address each misconception
- Provide examples that challenge common misconceptions
- Recommend questions that promote deeper understanding

Format your response as a clear, structured analysis that a teacher could use to guide instruction.
"""
        )
        self.chain = RunnableSequence(
            first=self.misconception_prompt,
            last=self.llm
        ) 