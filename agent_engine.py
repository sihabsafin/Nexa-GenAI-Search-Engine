"""
Nexa Search Agent Engine
Powered by LangChain + Groq with LangSmith tracing
"""

import os
from typing import Optional, List, Dict, Any
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import (
    DuckDuckGoSearchRun,
    WikipediaQueryRun,
    ArxivQueryRun
)
from langchain_community.utilities import (
    WikipediaAPIWrapper,
    ArxivAPIWrapper
)
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

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
        Priority: Llama 3.1 70B > Mixtral > Llama 3 70B
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
        Initialize the ReAct agent with custom prompt
        """
        # Enhanced ReAct prompt template
        template = """You are Nexa, an intelligent search assistant that helps users find accurate information.

You have access to these tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: think about what information you need and which tool to use
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now have enough information to answer
Final Answer: the final answer to the original input question

Guidelines:
- For recent news/events, use web_search first
- For facts/concepts/history, try wikipedia first
- For research/academic topics, check arxiv_search
- You can use multiple tools to cross-reference information
- Always cite sources when available
- Be concise but comprehensive
- If you don't find good results, try rephrasing the query

Question: {input}
Thought: {agent_scratchpad}"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad"],
            partial_variables={
                "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools]),
                "tool_names": ", ".join([tool.name for tool in self.tools])
            }
        )
        
        agent = create_react_agent(
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
                        tool_name = step[0].tool if hasattr(step[0], 'tool') else "Unknown"
                        sources.append({
                            "tool": tool_name,
                            "query": str(step[0].tool_input) if hasattr(step[0], 'tool_input') else ""
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
    """
    Main search function
    """
    engine = get_search_engine()
    return engine.search(query)
