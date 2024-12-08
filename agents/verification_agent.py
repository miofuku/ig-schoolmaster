from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
import json

class LearningVerificationAgent:
    def __init__(self, llm, chains):
        self.llm = llm
        self.chains = chains
        self.chat_history = ChatMessageHistory()
        
    async def verify_understanding(self, student_response, concept):
        """Verify student's understanding of a concept"""
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
        
    async def get_curriculum_standards(self, subject, grade, topic=None):
        """Get curriculum standards for a subject at specific grade"""
        result = await self.chains["curriculum_standards"].arun({
            "subject": subject,
            "grade": grade,
            "topic": topic or "general"
        })
        return json.loads(result)
    
    async def track_learning_progress(self, topic, standards, history, current_assessment):
        """Track progress against curriculum standards"""
        result = await self.chains["learning_progress"].arun({
            "topic": topic,
            "standards": standards,
            "history": history,
            "current_assessment": current_assessment
        })
        return result
    
    async def generate_targeted_assessment(self, standards, mastered_concepts):
        """Generate assessment based on curriculum standards and current mastery"""
        return await self.chains["knowledge_assessment"].arun({
            "knowledge_area": standards["topic"],
            "difficulty": "adaptive",
            "optional_material": "",
            "assessment_type": "progress",
            "curriculum_standards": standards,
            "mastered_concepts": mastered_concepts
        }) 