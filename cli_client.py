import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from chains.assessment_chain import ConceptVerificationChain
from chains.gap_analysis_chain import KnowledgeGapChain
from chains.knowledge_assessment_chain import KnowledgeAssessmentChain
from agents.verification_agent import LearningVerificationAgent
import json

load_dotenv()

class LearningCLI:
    def __init__(self):
        llm = ChatOpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        verification_chains = {
            "concept_verification": ConceptVerificationChain(llm),
            "knowledge_gap": KnowledgeGapChain(llm),
            "knowledge_assessment": KnowledgeAssessmentChain(llm)
        }
        
        self.agent = LearningVerificationAgent(llm, verification_chains)
    
    async def main_menu(self):
        while True:
            print("\n=== Learning Verification CLI ===")
            print("1. Verify Understanding")
            print("2. Generate Assessment")
            print("3. Analyze Progress")
            print("4. Curriculum Mapping")
            print("5. Exit")
            
            choice = input("\nSelect an option (1-5): ")
            
            if choice == "1":
                await self.verify_understanding()
            elif choice == "2":
                await self.generate_assessment()
            elif choice == "3":
                await self.analyze_progress()
            elif choice == "4":
                await self.curriculum_menu()
            elif choice == "5":
                break
            else:
                print("Invalid option. Please try again.")
    
    async def verify_understanding(self):
        concept = input("\nEnter the concept to verify: ")
        response = input("Enter your understanding of the concept: ")
        
        result = await self.agent.verify_understanding(response, concept)
        print("\nVerification Result:")
        print(result)
    
    async def generate_assessment(self):
        knowledge_area = input("\nEnter knowledge area: ")
        difficulty = input("Enter difficulty (beginner/intermediate/advanced): ")
        
        result = await self.agent.chains["knowledge_assessment"].arun({
            "knowledge_area": knowledge_area,
            "difficulty": difficulty,
            "optional_material": "",
            "assessment_type": "standard"
        })
        
        # Extract just the content from the response
        content = result.content if hasattr(result, 'content') else str(result)
        
        print("\nGenerated Assessment:")
        print(content)
    
    async def analyze_progress(self):
        # Simplified example data
        history = [
            {"concept": input("\nEnter a studied concept: "), 
             "score": input("Enter performance score (0-100): ")}
        ]
        competencies = [input("Enter target competency: ")]
        
        result = await self.agent.analyze_progress(history, competencies)
        print("\nProgress Analysis:")
        print(result)
    
    async def curriculum_menu(self):
        print("\n=== Curriculum Standards and Progress ===")
        subject = input("Enter subject (e.g., Mathematics): ")
        grade = input("Enter grade level (e.g., 9): ")
        topic = input("Enter specific topic (optional): ")
        
        # Get curriculum standards
        standards = await self.agent.get_curriculum_standards(subject, grade, topic)
        print("\nCurriculum Standards:")
        print(json.dumps(standards, indent=2))
        
        # Track progress if requested
        if input("\nWould you like to track progress? (y/n): ").lower() == 'y':
            history = input("Enter learning history file path (or press enter to skip): ")
            assessment = input("Enter recent assessment results (or press enter to skip): ")
            
            progress = await self.agent.track_learning_progress(
                topic or subject,
                standards,
                history,
                assessment
            )
            print("\nLearning Progress Analysis:")
            print(progress)
            
            # Generate targeted assessment
            if input("\nGenerate targeted assessment? (y/n): ").lower() == 'y':
                assessment = await self.agent.generate_targeted_assessment(
                    standards,
                    progress.get("mastered_concepts", [])
                )
                print("\nTargeted Assessment:")
                print(assessment)

def main():
    cli = LearningCLI()
    asyncio.run(cli.main_menu())

if __name__ == "__main__":
    main() 