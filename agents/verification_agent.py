from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.memory import ConversationBufferMemory

class LearningVerificationAgent:
    def __init__(self, llm, chains):
        self.llm = llm
        self.chains = chains
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        
    async def verify_understanding(self, student_response, concept):
        result = await self.chains["concept_verification"].arun({
            "response": student_response,
            "concept": concept
        })
        self.memory.save_context({"input": concept}, {"output": result})
        return result
    
    async def analyze_progress(self, assessment_history, target_competencies):
        # Include memory in analysis
        chat_history = self.memory.load_memory_variables({})["chat_history"]
        
        return await self.chains["knowledge_gap"].arun({
            "history": assessment_history,
            "competencies": target_competencies,
            "chat_history": chat_history
        })
    
    async def generate_revision_task(self, subject, knowledge_areas, assessment_history):
        """Generate revision tasks based on learning history"""
        # Analyze past performance
        gaps = await self.analyze_progress(assessment_history, knowledge_areas)
        
        # Generate focused assessment
        return await self.chains["knowledge_assessment"].arun({
            "knowledge_area": knowledge_areas,
            "difficulty": "adaptive",
            "optional_material": "",
            "assessment_type": "revision",
            "learning_gaps": gaps
        }) 