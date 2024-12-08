from langchain_community.chat_message_histories import ChatMessageHistory
import json
from typing import Dict

class LearningVerificationAgent:
    def __init__(self, llm, chains):
        self.llm = llm
        self.chains = chains
        self.chat_history = ChatMessageHistory()
        
    async def generate_targeted_assessment(self, context: Dict, assessment_type: str):
        """Generate assessment based on curriculum context and learning progress"""
        return await self.chains["knowledge_assessment"].arun({
            "knowledge_area": f"{context['subject']} - {context['topic']}",
            "difficulty": "adaptive",
            "key_points": context["key_points"],
            "progress": context["progress"],
            "assessment_type": assessment_type
        })
    
    async def track_progress(self, context: Dict, assessment_result: Dict):
        """Track and analyze learning progress"""
        result = await self.chains["learning_progress"].arun({
            "context": context,
            "current_result": assessment_result
        })
        return json.loads(result)