import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from chains.knowledge_assessment_chain import KnowledgeAssessmentChain
from chains.misconception_chain import MisconceptionDetectionChain
from chains.depth_analysis_chain import KnowledgeDepthChain
from agents.verification_agent import LearningVerificationAgent
from curriculum.context_manager import CurriculumContext

load_dotenv()

class LearningCLI:
    def __init__(self):
        self.context_manager = CurriculumContext()
        llm = ChatOpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        verification_chains = {
            "misconception_detection": MisconceptionDetectionChain(llm),
            "depth_analysis": KnowledgeDepthChain(llm),
            "knowledge_assessment": KnowledgeAssessmentChain(llm)
        }
        
        self.agent = LearningVerificationAgent(llm, verification_chains)
    
    async def main_menu(self):
        while True:
            print("\n=== Learning Management System ===")
            print("1. Manage Curriculum")
            print("2. Add Topic Points")
            print("3. Generate Assessment")
            print("4. View Progress")
            print("5. Exit")
            
            choice = input("\nSelect an option (1-5): ")
            
            if choice == "1":
                await self.manage_curriculum()
            elif choice == "2":
                await self.add_topic_points()
            elif choice == "3":
                await self.generate_contextual_assessment()
            elif choice == "4":
                await self.view_progress()
            elif choice == "5":
                break
    
    async def manage_curriculum(self):
        print("\n=== Curriculum Management ===")
        subject = input("Enter subject name: ")
        print("Enter topics (one per line, empty line to finish):")
        topics = []
        while True:
            topic = input("> ")
            if not topic:
                break
            topics.append(topic)
        
        self.context_manager.add_subject(subject, topics)
        print(f"\nAdded {len(topics)} topics to {subject}")
    
    async def add_topic_points(self):
        print("\n=== Add Topic Points ===")
        subject = input("Enter subject name: ")
        topic = input("Enter topic name: ")
        print("Enter key points (one per line, empty line to finish):")
        points = []
        while True:
            point = input("> ")
            if not point:
                break
            points.append(point)
        
        self.context_manager.add_topic_points(subject, topic, points)
        print(f"\nAdded {len(points)} key points to {topic}")
    
    async def generate_contextual_assessment(self):
        print("\n=== Generate Assessment ===")
        subject = input("Enter subject: ")
        topic = input("Enter topic: ")
        assessment_type = input("Assessment type (daily/weekly/topic): ")
        
        # Get context for assessment
        context = self.context_manager.get_topic_context(subject, topic)
        
        result = await self.agent.generate_targeted_assessment({
            "subject": subject,
            "topic": topic,
            "key_points": context["key_points"],
            "progress": context["progress"]
        }, assessment_type)
        
        print("\nGenerated Assessment:")
        print(result)
    
    async def view_progress(self):
        print("\n=== Learning Progress Analysis ===")
        subject = input("Enter subject name: ")
        
        # Get all verifications for the subject
        subject_context = self.context_manager.get_subject_context(subject)
        
        # Analyze trends
        trend_analysis = await self.agent.analyze_learning_trends(subject_context)
        
        print("\nLearning Trends:")
        print("Understanding Progression:")
        print(trend_analysis["trend_analysis"]["understanding_progression"])
        print("\nPersistent Misconceptions:")
        print(trend_analysis["trend_analysis"]["persistent_misconceptions"])
        print("\nDepth Development:")
        print(trend_analysis["trend_analysis"]["depth_development"])
        print("\nRecommendations:")
        print(trend_analysis["trend_analysis"]["recommendations"])
        print("\nAI Insights:")
        print(trend_analysis["ai_insights"])

def main():
    cli = LearningCLI()
    asyncio.run(cli.main_menu())

if __name__ == "__main__":
    main() 