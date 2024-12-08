from langchain.prompts import PromptTemplate

class KnowledgeDepthChain:
    def __init__(self, llm):
        self.llm = llm
        self.depth_prompt = PromptTemplate(
            input_variables=["response", "topic", "expected_level"],
            template="""
            Analyze the depth of understanding in this response:
            
            Topic: {topic}
            Expected Level: {expected_level}
            Response: {response}
            
            Evaluate:
            1. Surface understanding vs. deep comprehension
            2. Use of domain-specific vocabulary
            3. Ability to explain relationships and connections
            4. Application of concepts to new situations
            5. Critical thinking indicators
            
            Provide specific examples from the response for each point.
            """
        ) 