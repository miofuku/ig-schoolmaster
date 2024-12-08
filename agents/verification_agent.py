from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

class LearningVerificationAgent:
    def __init__(self, llm, chains):
        self.llm = llm
        self.chains = chains
        self.chat_history = ChatMessageHistory()
        
    async def verify_understanding(self, student_response, concept):
        result = await self.chains["concept_verification"].arun({
            "concept": concept,
            "response": student_response
        })
        
        # Extract just the content string from the response
        content = result.content if hasattr(result, 'content') else str(result)
        
        self.chat_history.add_messages([
            HumanMessage(content=concept),
            AIMessage(content=content)
        ])
        return content
    
    async def analyze_progress(self, assessment_history, target_competencies):
        # Include memory in analysis
        messages = self.chat_history.messages
        
        return await self.chains["knowledge_gap"].arun({
            "history": assessment_history,
            "competencies": target_competencies,
            "chat_history": [m.content for m in messages]
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