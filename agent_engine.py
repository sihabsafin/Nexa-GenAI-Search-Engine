"""
Nexa Search Agent Engine - Fixed for Latest LangChain
Powered by LangChain + Groq with LangSmith tracing
"""

import os
from typing import Optional, List, Dict, Any
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools import (
    DuckDuckGoSearchRun,
    WikipediaQueryRun,
    ArxivQueryRun
)
from langchain_community.utilities import (
    WikipediaAPIWrapper,
    ArxivAPIWrapper
)

# LangSmith Configuration (Optional but recommended)
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
            raise ValueError("GROQ_API_KEY not found. Please set it in your environment.")
        
        self.llm = self._initialize_llm()
        self.tools = self._initialize_tools()
        self.agent = self._initialize_agent()
    
    def _initialize_llm(self) -> ChatGroq:
        """
        Initialize the LLM with the best available free model
        Priority: Llama 3.3 70B > Llama 3.1 70B > Mixtral > Llama 3 70B
        """
        models = [
            "llama-3.3-70b-versatile",  # Latest and most powerful
            "llama-3.1-70b-versatile",  # Excellent for reasoning
            "mixtral-8x7b-32768",       # Great context window
            "llama3-70b-8192",          # Reliable fallback
        ]
        
        for model in models:
            try:
                llm = ChatGroq(
                    api_key=self.api_key,
                    model=model,
                    temperature=0.3,
                    max_tokens=4096,
                    timeout=30,
                    max_retries=2,
                )
                # Test the model
                llm.invoke("test")
                print(f"✓ Using model: {model}")
                return llm
            except Exception as e:
                print(f"✗ Model {model} unavailable: {str(e)[:50]}")
                continue
        
        raise RuntimeError("No Groq models available. Check your API key and quota.")
    
    def _initialize_tools(self) -> List:
        """
        Initialize enhanced search tools with better configurations
        """
        # Web Search Tool - Enhanced
        search_tool = DuckDuckGoSearchRun(
            name="web_search",
            description=(
                "Search the internet for current information, news, facts, and real-time data. "
                "Use this for: recent events, current news, product info, trending topics, "
                "company information, and any query requiring up-to-date web results."
            )
        )
        
        # Wikipedia Tool - Enhanced
        wiki_tool = WikipediaQueryRun(
            name="wikipedia",
            description=(
                "Search Wikipedia for encyclopedic knowledge, historical facts, biographies, "
                "scientific concepts, and well-established information. "
                "Use this for: definitions, historical events, notable people, scientific concepts, "
                "geographical information, and general knowledge queries."
            ),
            api_wrapper=WikipediaAPIWrapper(
                top_k_results=2,
                doc_content_chars_max=1000,
                load_all_available_meta=True
            )
        )
        
        # arXiv Tool - Enhanced
        arxiv_tool = ArxivQueryRun(
            name="arxiv_search",
            description=(
                "Search arXiv for academic papers, research articles, and scientific publications. "
                "Use this for: research papers, academic studies, scientific discoveries, "
                "technical papers, preprints in physics, math, CS, biology, and other sciences."
            ),
            api_wrapper=ArxivAPIWrapper(
                top_k_results=3,
                doc_content_chars_max=1000,
                load_all_available_meta=True
            )
        )
        
        return [search_tool, wiki_tool, arxiv_tool]
    
    def _initialize_agent(self) -> AgentExecutor:
        """
        Initialize the tool-calling agent (compatible with latest LangChain)
        """
        # Create prompt template for tool-calling agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Nexa, an intelligent search assistant that helps users find accurate information.

You have access to multiple search tools. Choose the most appropriate tool(s) based on the user's query:

- For recent news/events, use web_search first
- For facts/concepts/history, try wikipedia first  
- For research/academic topics, check arxiv_search
- You can use multiple tools to cross-reference information

Guidelines:
- Always cite sources when available
- Be concise but comprehensive
- If you don't find good results, try rephrasing the query
- Provide clear, well-structured answers"""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=LANGSMITH_ENABLED,
            handle_parsing_errors=True,
            max_iterations=6,
            max_execution_time=60,
            return_intermediate_steps=True
        )
    
    def search(self, query: str) -> Dict[str, Any]:
        """
        Execute search and return structured results
        """
        try:
            result = self.agent.invoke({"input": query})
            
            # Extract sources from intermediate steps
            sources = []
            if "intermediate_steps" in result:
                for step in result["intermediate_steps"]:
                    if len(step) >= 2:
                        action = step[0]
                        tool_name = action.tool if hasattr(action, 'tool') else "Unknown"
                        tool_input = str(action.tool_input) if hasattr(action, 'tool_input') else ""
                        
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
            error_msg = str(e)
            return {
                "answer": f"I encountered an error while searching: {error_msg}",
                "sources": [],
                "success": False,
                "error": error_msg
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
    """
    Main search function
    """
    engine = get_search_engine()
    return engine.search(query)
