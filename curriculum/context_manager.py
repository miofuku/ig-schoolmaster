import json
from pathlib import Path
from typing import Dict, List, Optional

class CurriculumContext:
    def __init__(self, context_file: str = "curriculum_context.json"):
        self.context_file = Path(context_file)
        self.context = self._load_context()
    
    def _load_context(self) -> Dict:
        if self.context_file.exists():
            return json.loads(self.context_file.read_text())
        return {
            "subjects": {},
            "learning_progress": {},
            "assessment_history": []
        }
    
    def _save_context(self):
        self.context_file.write_text(json.dumps(self.context, indent=2))
    
    def add_subject(self, subject: str, topics: List[str]):
        """Add or update a subject and its topics"""
        self.context["subjects"][subject] = {
            "topics": topics,
            "key_points": {},
            "progress": {}
        }
        self._save_context()
    
    def add_topic_points(self, subject: str, topic: str, points: List[str]):
        """Add key learning points for a topic"""
        if subject not in self.context["subjects"]:
            raise ValueError(f"Subject {subject} not found")
        
        self.context["subjects"][subject]["key_points"][topic] = points
        self._save_context()
    
    def update_progress(self, subject: str, topic: str, assessment_result: Dict):
        """Update learning progress for a topic"""
        if subject not in self.context["subjects"]:
            raise ValueError(f"Subject {subject} not found")
        
        progress = self.context["subjects"][subject]["progress"]
        if topic not in progress:
            progress[topic] = []
        
        progress[topic].append(assessment_result)
        self.context["assessment_history"].append({
            "subject": subject,
            "topic": topic,
            "result": assessment_result,
            "timestamp": assessment_result.get("timestamp")
        })
        self._save_context()
    
    def get_subject_context(self, subject: str) -> Dict:
        """Get all context for a subject"""
        return self.context["subjects"].get(subject, {})
    
    def get_topic_context(self, subject: str, topic: str) -> Dict:
        """Get context for a specific topic"""
        subject_context = self.get_subject_context(subject)
        return {
            "key_points": subject_context.get("key_points", {}).get(topic, []),
            "progress": subject_context.get("progress", {}).get(topic, [])
        } 