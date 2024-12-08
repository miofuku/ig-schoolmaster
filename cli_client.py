import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from chains.assessment_chain import ConceptVerificationChain
from chains.gap_analysis_chain import KnowledgeGapChain
from chains.knowledge_assessment_chain import KnowledgeAssessmentChain
from agents.verification_agent import LearningVerificationAgent

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
            print("4. Exit")
            
            choice = input("\nSelect an option (1-4): ")
            
            if choice == "1":
                await self.verify_understanding()
            elif choice == "2":
                await self.generate_assessment()
            elif choice == "3":
                await self.analyze_progress()
            elif choice == "4":
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
        
        print("\nGenerated Assessment:")
        print(result)
    
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

def main():
    cli = LearningCLI()
    asyncio.run(cli.main_menu())

if __name__ == "__main__":
    main() 