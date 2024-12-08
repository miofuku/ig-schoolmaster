from langchain_community.chat_message_histories import ChatMessageHistory
import json
from typing import Dict
from analysis.trend_analyzer import LearningTrendAnalyzer

class LearningVerificationAgent:
    def __init__(self, llm, chains):
        self.llm = llm
        self.chains = chains
        self.chat_history = ChatMessageHistory()
        self.trend_analyzer = LearningTrendAnalyzer()
        
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
    
    async def verify_understanding(self, context: Dict, student_response: str):
        """Comprehensive verification of student understanding"""
        # Basic assessment
        assessment = await self.chains["knowledge_assessment"].arun({
            "knowledge_area": f"{context['subject']} - {context['topic']}",
            "student_response": student_response,
            "key_points": context["key_points"]
        })
        
        # Misconception detection
        misconceptions = await self.chains["misconception_detection"].arun({
            "subject": context["subject"],
            "topic": context["topic"],
            "student_response": student_response,
            "key_points": context["key_points"]
        })
        
        # Depth analysis
        depth = await self.chains["knowledge_depth"].arun({
            "response": student_response,
            "topic": context["topic"],
            "expected_level": context.get("expected_level", "intermediate")
        })
        
        return {
            "assessment": assessment,
            "misconceptions": misconceptions,
            "depth_analysis": depth,
            "verification_summary": await self._generate_summary(assessment, misconceptions, depth)
        }
    
    async def _generate_summary(self, assessment, misconceptions, depth):
        """Generate a concise summary of all analyses"""
        return await self.chains["summary"].arun({
            "assessment": assessment,
            "misconceptions": misconceptions,
            "depth_analysis": depth
        })
    
    async def analyze_learning_trends(self, context: Dict):
        """Analyze learning trends across topics"""
        verifications = context.get("verifications", [])
        
        trend_analysis = self.trend_analyzer.analyze_verification_history(verifications)
        
        # Generate AI insights on the trends
        insights = await self.chains["knowledge_assessment"].arun({
            "analysis": trend_analysis,
            "context": context,
            "assessment_type": "trend_analysis"
        })
        
        return {
            "trend_analysis": trend_analysis,
            "ai_insights": insights
        }