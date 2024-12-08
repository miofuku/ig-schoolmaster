import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

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
    
    def add_verification_result(self, subject: str, topic: str, verification: Dict):
        """Store verification results with metadata"""
        if subject not in self.context["subjects"]:
            raise ValueError(f"Subject {subject} not found")
        
        if "verifications" not in self.context["subjects"][subject]:
            self.context["subjects"][subject]["verifications"] = {}
        
        topic_verifications = self.context["subjects"][subject]["verifications"]
        if topic not in topic_verifications:
            topic_verifications[topic] = []
        
        topic_verifications[topic].append({
            "timestamp": datetime.now().isoformat(),
            "result": verification,
            "metrics": {
                "misconception_count": len(verification["misconceptions"]),
                "depth_score": self._calculate_depth_score(verification["depth_analysis"]),
                "understanding_level": self._assess_understanding_level(verification)
            }
        })
        self._save_context()
    
    def get_verification_history(self, subject: str, topic: str = None) -> List[Dict]:
        """Get verification history for trend analysis"""
        if subject not in self.context["subjects"]:
            raise ValueError(f"Subject {subject} not found")
            
        verifications = self.context["subjects"][subject].get("verifications", {})
        
        if topic:
            return verifications.get(topic, [])
        
        # Return all verifications for the subject if no topic specified
        all_verifications = []
        for topic_verifications in verifications.values():
            all_verifications.extend(topic_verifications)
        
        # Sort by timestamp
        return sorted(all_verifications, key=lambda x: x["timestamp"])