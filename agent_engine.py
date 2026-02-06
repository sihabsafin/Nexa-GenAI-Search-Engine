"""
Nexa Search Agent Engine
Compatible with LangChain 0.1.x and Python 3.10-3.11
"""

import os
from typing import Optional, List, Dict, Any
from langchain_groq import ChatGroq
from langchain_community.tools import (
    DuckDuckGoSearchRun,
    WikipediaQueryRun,
    ArxivQueryRun
)
from langchain_community.utilities import (
    WikipediaAPIWrapper,
    ArxivAPIWrapper
)
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent

# LangSmith Configuration (Optional)
LANGSMITH_ENABLED = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
if LANGSMITH_ENABLED:
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "nexa-search")

class NexaSearchEngine:
    """
    Advanced search engine with multiple LLM models and enhanced tools
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found. Please set it in Streamlit Secrets.")
        
        self.llm = self._initialize_llm()
        self.tools = self._initialize_tools()
        self.agent = self._initialize_agent()
    
    def _initialize_llm(self) -> ChatGroq:
        """
        Initialize the LLM with the best available free model
        """
        models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
            "llama3-70b-8192",
        ]
        
        for model in models:
            try:
                llm = ChatGroq(
                    api_key=self.api_key,
                    model=model,
                    temperature=0.3,
                    max_tokens=4096,
                )
                # Test the model
                llm.invoke("test")
                print(f"✓ Using model: {model}")
                return llm
            except Exception as e:
                print(f"✗ Model {model} unavailable")
                continue
        
        raise RuntimeError("No Groq models available. Check your API key.")
    
    def _initialize_tools(self) -> List:
        """
        Initialize search tools
        """
        # Web Search
        search_tool = DuckDuckGoSearchRun(
            name="web_search",
            description="Search the internet for current information, news, and real-time data."
        )
        
        # Wikipedia
        wiki_tool = WikipediaQueryRun(
            name="wikipedia",
            description="Search Wikipedia for encyclopedic knowledge and facts.",
            api_wrapper=WikipediaAPIWrapper(
                top_k_results=2,
                doc_content_chars_max=1000
            )
        )
        
        # arXiv
        arxiv_tool = ArxivQueryRun(
            name="arxiv_search",
            description="Search arXiv for academic papers and research articles.",
            api_wrapper=ArxivAPIWrapper(
                top_k_results=2,
                doc_content_chars_max=1000
            )
        )
        
        return [search_tool, wiki_tool, arxiv_tool]
    
    def _initialize_agent(self) -> AgentExecutor:
        """
        Initialize the agent using ReAct agent (compatible with Groq)
        """
        prompt = PromptTemplate.from_template("""You are Nexa, an intelligent search assistant. Answer questions using the available tools when needed.

Available tools:
{tools}

IMPORTANT INSTRUCTIONS:
- Use tools ONLY when you need current/specific information
- For general knowledge questions, answer directly without using tools
- After getting tool results, immediately provide the Final Answer
- Keep tool usage to 1-2 calls maximum

Format:
Question: the input question you must answer
Thought: do I need to use a tool or can I answer directly?
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat only if absolutely necessary)
Thought: I now know the final answer
Final Answer: provide a clear, comprehensive answer

Question: {input}
Thought:{agent_scratchpad}""")
        
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=10,
            max_execution_time=60,
            early_stopping_method="generate",
            return_intermediate_steps=True
        )
    
    def search(self, query: str) -> Dict[str, Any]:
        """
        Execute search and return results
        """
        try:
            result = self.agent.invoke({"input": query})
            
            # Extract sources
            sources = []
            if "intermediate_steps" in result:
                for step in result["intermediate_steps"]:
                    if len(step) >= 2:
                        action = step[0]
                        tool_name = getattr(action, 'tool', 'Unknown')
                        tool_input = str(getattr(action, 'tool_input', ''))
                        
                        sources.append({
                            "tool": tool_name,
                            "query": tool_input
                        })
            
            return {
                "answer": result.get("output", "No answer generated."),
                "sources": sources,
                "success": True
            }
            
        except Exception as e:
            return {
                "answer": f"Search error: {str(e)}",
                "sources": [],
                "success": False,
                "error": str(e)
            }

# Global instance
_engine = None

def get_search_engine() -> NexaSearchEngine:
    """Get or create search engine instance"""
    global _engine
    if _engine is None:
        _engine = NexaSearchEngine()
    return _engine

def run_search(query: str) -> Dict[str, Any]:
    """Main search function"""
    engine = get_search_engine()
    return engine.search(query)
