from langchain.prompts import PromptTemplate

class KnowledgeDepthChain:
    def __init__(self, llm):
        self.llm = llm
        self.depth_prompt = PromptTemplate(
            input_variables=["response", "topic", "expected_level"],
            template="""You are an expert in assessing student understanding using Bloom's Taxonomy and SOLO Taxonomy.

Analyze this student response for depth of understanding:

Topic: {topic}
Expected Level: {expected_level}
Student Response: {response}

1. Knowledge Structure Analysis:
- Identify the level of understanding (surface/deep/relational)
- Evaluate use of subject-specific vocabulary and concepts
- Assess connections made between different ideas

2. Cognitive Skills Demonstrated:
- Knowledge recall and comprehension
- Application of concepts
- Analysis and synthesis
- Evaluation and creation

3. Critical Thinking Indicators:
- Evidence of independent thinking
- Ability to transfer knowledge
- Problem-solving approaches
- Metacognitive awareness

4. Areas for Development:
- Identify opportunities for deeper understanding
- Suggest specific questions to probe understanding
- Recommend activities to enhance conceptual connections

Provide specific examples from the response to support your analysis.
Rate each aspect on a scale of 1-5 with clear justification.
"""
        ) 