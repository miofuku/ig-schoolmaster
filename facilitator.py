from langchain.agents import initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class AIFacilitator:
    def __init__(self, llm):
        self.llm = llm
        self.chains = self._initialize_chains()
        self.agents = self._initialize_agents()
    
    def _initialize_chains(self):
        # Create specialized chains for different tasks
        knowledge_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["query"],
                template="Given the knowledge request: {query}\nProvide a detailed explanation:"
            )
        )
        
        analysis_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["content"],
                template="Analyze the following content and provide insights: {content}"
            )
        )
        
        return {
            "knowledge": knowledge_chain,
            "analysis": analysis_chain
        }
    
    def _initialize_agents(self):
        tools = [
            Tool(
                name="Knowledge Search",
                func=self.chains["knowledge"].run,
                description="Useful for finding specific information"
            ),
            Tool(
                name="Content Analysis",
                func=self.chains["analysis"].run,
                description="Useful for analyzing and understanding content"
            )
        ]
        
        agent = initialize_agent(
            tools,
            self.llm,
            agent="zero-shot-react-description",
            verbose=True
        )
        
        return {"main": agent}
    
    async def process_request(self, request):
        # Use the appropriate chain or agent based on the request type
        try:
            response = await self.agents["main"].arun(request)
            return response
        except Exception as e:
            return f"Error processing request: {str(e)}"