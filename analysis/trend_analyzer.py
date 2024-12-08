from typing import List, Dict
from datetime import datetime
from collections import Counter

class LearningTrendAnalyzer:
    def analyze_verification_history(self, verifications: List[Dict]) -> Dict:
        """Analyze trends in verification results over time"""
        if not verifications:
            return self._empty_analysis()
        
        return {
            "understanding_progression": self._analyze_understanding_progression(verifications),
            "persistent_misconceptions": self._identify_persistent_misconceptions(verifications),
            "depth_development": self._analyze_depth_development(verifications),
            "recommendations": self._generate_recommendations(verifications)
        }
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure when no data is available"""
        return {
            "understanding_progression": {"trend": "No data", "details": []},
            "persistent_misconceptions": [],
            "depth_development": {"trend": "No data", "scores": []},
            "recommendations": ["Start by adding some verification results"]
        }
    
    def _analyze_understanding_progression(self, verifications: List[Dict]) -> Dict:
        """Analyze how understanding has progressed over time"""
        progression = []
        
        # Sort verifications by timestamp
        sorted_verifications = sorted(verifications, 
                                   key=lambda x: datetime.fromisoformat(x["timestamp"]))
        
        for verification in sorted_verifications:
            metrics = verification["metrics"]
            progression.append({
                "timestamp": verification["timestamp"],
                "understanding_level": metrics["understanding_level"],
                "topic": verification["result"].get("topic", "unknown")
            })
        
        # Determine overall trend
        if len(progression) >= 2:
            initial_level = progression[0]["understanding_level"]
            final_level = progression[-1]["understanding_level"]
            trend = "improving" if final_level > initial_level else \
                   "declining" if final_level < initial_level else "stable"
        else:
            trend = "insufficient data"
        
        return {
            "trend": trend,
            "details": progression
        }
    
    def _identify_persistent_misconceptions(self, verifications: List[Dict]) -> List[Dict]:
        """Identify misconceptions that appear repeatedly"""
        misconception_counter = Counter()
        
        for verification in verifications:
            misconceptions = verification["result"].get("misconceptions", [])
            misconception_counter.update(misconceptions)
        
        # Filter for misconceptions that appear multiple times
        persistent = [
            {
                "misconception": concept,
                "frequency": count,
                "impact": "high" if count > len(verifications) / 2 else "medium"
            }
            for concept, count in misconception_counter.items()
            if count > 1
        ]
        
        return sorted(persistent, key=lambda x: x["frequency"], reverse=True)
    
    def _analyze_depth_development(self, verifications: List[Dict]) -> Dict:
        """Analyze how knowledge depth has developed"""
        depth_scores = []
        
        sorted_verifications = sorted(verifications, 
                                    key=lambda x: datetime.fromisoformat(x["timestamp"]))
        
        for verification in sorted_verifications:
            depth_scores.append({
                "timestamp": verification["timestamp"],
                "score": verification["metrics"]["depth_score"],
                "topic": verification["result"].get("topic", "unknown")
            })
        
        # Calculate trend
        if len(depth_scores) >= 2:
            initial_score = depth_scores[0]["score"]
            final_score = depth_scores[-1]["score"]
            trend = "deepening" if final_score > initial_score else \
                   "superficial" if final_score < initial_score else "consistent"
        else:
            trend = "insufficient data"
        
        return {
            "trend": trend,
            "scores": depth_scores
        }
    
    def _generate_recommendations(self, verifications: List[Dict]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Get latest verification
        latest = max(verifications, key=lambda x: datetime.fromisoformat(x["timestamp"]))
        
        # Understanding level recommendations
        if latest["metrics"]["understanding_level"] < 0.7:
            recommendations.append(
                "Focus on strengthening fundamental concepts before moving to advanced topics"
            )
        
        # Depth recommendations
        if latest["metrics"]["depth_score"] < 0.6:
            recommendations.append(
                "Practice explaining concepts in your own words and connecting ideas"
            )
        
        # Misconception recommendations
        persistent = self._identify_persistent_misconceptions(verifications)
        if persistent:
            recommendations.append(
                f"Address persistent misconceptions, especially: {persistent[0]['misconception']}"
            )
        
        # Frequency recommendations
        timestamps = [datetime.fromisoformat(v["timestamp"]) for v in verifications]
        if timestamps:
            avg_gap = (max(timestamps) - min(timestamps)).days / len(timestamps)
            if avg_gap > 7:
                recommendations.append(
                    "Consider increasing the frequency of learning verification sessions"
                )
        
        return recommendations or ["Continue with current learning approach"]