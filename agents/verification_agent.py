from langchain.agents import Agent
from typing import List, Dict

class LearningVerificationAgent(Agent):
    def __init__(self, llm, chains):
        self.llm = llm
        self.chains = chains
        
    async def verify_understanding(self, 
                                 student_response: str, 
                                 concept: str) -> Dict:
        result = await self.chains["concept_verification"].arun({
            "student_response": student_response,
            "concept": concept
        })
        return self._format_verification_result(result)
        
    async def analyze_progress(self, 
                             assessment_history: List[Dict], 
                             target_competencies: List[str]) -> Dict:
        result = await self.chains["knowledge_gap"].arun({
            "assessment_history": assessment_history,
            "target_competencies": target_competencies
        })
        return self._format_progress_analysis(result) 