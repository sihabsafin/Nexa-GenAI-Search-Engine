"""
Nexa Search Agent Engine - Enhanced Version
Features: Streaming, Caching, Multiple Modes, Multi-language
"""

import os
import json
import hashlib
from typing import Optional, List, Dict, Any, Iterator
from datetime import datetime, timedelta
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
from langchain.callbacks.base import BaseCallbackHandler

# LangSmith Configuration (Optional)
LANGSMITH_ENABLED = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
if LANGSMITH_ENABLED:
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "nexa-search")


class StreamingCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming responses"""
    
    def __init__(self, callback_func):
        self.callback_func = callback_func
        self.current_step = ""
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Called when new token is generated"""
        if self.callback_func:
            self.callback_func(token)
    
    def on_tool_start(self, serialized: dict, input_str: str, **kwargs) -> None:
        """Called when tool starts"""
        tool_name = serialized.get("name", "Unknown")
        self.current_step = f"🔍 Using {tool_name}..."
        if self.callback_func:
            self.callback_func(f"\n\n{self.current_step}\n")
    
    def on_tool_end(self, output: str, **kwargs) -> None:
        """Called when tool completes"""
        if self.callback_func:
            self.callback_func(f"✓ Complete\n\n")


class SearchCache:
    """Simple in-memory cache for search results"""
    
    def __init__(self, ttl_minutes: int = 30):
        self.cache = {}
        self.ttl = timedelta(minutes=ttl_minutes)
    
    def _get_key(self, query: str, mode: str, sources: List[str]) -> str:
        """Generate cache key"""
        key_data = f"{query}_{mode}_{'_'.join(sorted(sources))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, query: str, mode: str, sources: List[str]) -> Optional[Dict]:
        """Get cached result"""
        key = self._get_key(query, mode, sources)
        if key in self.cache:
            cached_data, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return cached_data
            else:
                del self.cache[key]
        return None
    
    def set(self, query: str, mode: str, sources: List[str], result: Dict):
        """Cache result"""
        key = self._get_key(query, mode, sources)
        self.cache[key] = (result, datetime.now())
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()


class NexaSearchEngine:
    """
    Advanced search engine with multiple modes and streaming support
    """
    
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ko': 'Korean',
        'ar': 'Arabic'
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found. Please set it in Streamlit Secrets.")
        
        self.cache = SearchCache(ttl_minutes=30)
        self.llm = self._initialize_llm()
        self.all_tools = self._initialize_all_tools()
        self.agents = {}  # Cache agents for different configurations
    
    def _initialize_llm(self) -> ChatGroq:
        """Initialize the LLM with the best available free model"""
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
                    streaming=True,  # Enable streaming
                )
                # Test the model
                llm.invoke("test")
                print(f"✓ Using model: {model}")
                return llm
            except Exception as e:
                print(f"✗ Model {model} unavailable")
                continue
        
        raise RuntimeError("No Groq models available. Check your API key.")
    
    def _initialize_all_tools(self) -> Dict[str, Any]:
        """Initialize all available search tools"""
        tools = {}
        
        # Web Search
        try:
            tools['web_search'] = DuckDuckGoSearchRun(
                name="web_search",
                description="Search the internet for current information, news, and real-time data."
            )
        except:
            print("⚠️ Web search tool unavailable")
        
        # Wikipedia
        try:
            tools['wikipedia'] = WikipediaQueryRun(
                name="wikipedia",
                description="Search Wikipedia for encyclopedic knowledge and facts.",
                api_wrapper=WikipediaAPIWrapper(
                    top_k_results=2,
                    doc_content_chars_max=1000
                )
            )
        except:
            print("⚠️ Wikipedia tool unavailable")
        
        # arXiv
        try:
            tools['arxiv_search'] = ArxivQueryRun(
                name="arxiv_search",
                description="Search arXiv for academic papers and research articles.",
                api_wrapper=ArxivAPIWrapper(
                    top_k_results=2,
                    doc_content_chars_max=1000
                )
            )
        except:
            print("⚠️ arXiv tool unavailable")
        
        return tools
    
    def _get_agent(self, mode: str, selected_sources: List[str], language: str = 'en') -> AgentExecutor:
        """Get or create agent for specific configuration"""
        config_key = f"{mode}_{language}_{'_'.join(sorted(selected_sources))}"
        
        if config_key in self.agents:
            return self.agents[config_key]
        
        # Select tools based on sources
        tools = [self.all_tools[src] for src in selected_sources if src in self.all_tools]
        
        if not tools:
            raise ValueError("No valid tools selected")
        
        # Configure based on mode
        if mode == "quick":
            max_iterations = 3
            prompt_instruction = "Provide a concise, direct answer using minimal tool calls."
        elif mode == "deep":
            max_iterations = 15
            prompt_instruction = "Provide a comprehensive, detailed answer with thorough research."
        else:  # balanced (default)
            max_iterations = 10
            prompt_instruction = "Provide a clear, balanced answer with appropriate detail."
        
        # Language instruction
        lang_name = self.SUPPORTED_LANGUAGES.get(language, 'English')
        lang_instruction = f"Respond in {lang_name}." if language != 'en' else ""
        
        # Create prompt
        prompt = PromptTemplate.from_template(f"""You are Nexa, an intelligent search assistant. {prompt_instruction} {lang_instruction}

Available tools:
{{tools}}

IMPORTANT INSTRUCTIONS:
- Use tools when you need current/specific information
- For general knowledge, answer directly without tools
- After getting tool results, provide the Final Answer immediately
- Be clear, accurate, and helpful

Format:
Question: the input question you must answer
Thought: do I need to use a tool or can I answer directly?
Action: the action to take, should be one of [{{tool_names}}]
Action Input: the input to the action
Observation: the result of the action
... (repeat only if necessary)
Thought: I now know the final answer
Final Answer: provide a clear answer

Question: {{input}}
Thought:{{agent_scratchpad}}""")
        
        # Create agent
        agent = create_react_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt
        )
        
        # Create executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=max_iterations,
            max_execution_time=90,
            early_stopping_method="generate",
            return_intermediate_steps=True
        )
        
        self.agents[config_key] = agent_executor
        return agent_executor
    
    def search(
        self, 
        query: str, 
        mode: str = "balanced",
        selected_sources: Optional[List[str]] = None,
        language: str = "en",
        use_cache: bool = True,
        stream_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Execute search with specified parameters
        
        Args:
            query: Search query
            mode: "quick", "balanced", or "deep"
            selected_sources: List of sources to use (default: all)
            language: Language code for response
            use_cache: Whether to use cached results
            stream_callback: Callback function for streaming
        """
        # Default sources
        if selected_sources is None:
            selected_sources = list(self.all_tools.keys())
        
        # Validate sources
        selected_sources = [s for s in selected_sources if s in self.all_tools]
        if not selected_sources:
            return {
                "answer": "Error: No valid search sources selected.",
                "sources": [],
                "success": False,
                "error": "Invalid sources"
            }
        
        # Check cache
        if use_cache:
            cached_result = self.cache.get(query, mode, selected_sources)
            if cached_result:
                cached_result['from_cache'] = True
                return cached_result
        
        try:
            # Get agent
            agent = self._get_agent(mode, selected_sources, language)
            
            # Setup streaming if callback provided
            callbacks = []
            if stream_callback:
                callbacks.append(StreamingCallbackHandler(stream_callback))
            
            # Execute search
            result = agent.invoke(
                {"input": query},
                config={"callbacks": callbacks} if callbacks else None
            )
            
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
            
            search_result = {
                "answer": result.get("output", "No answer generated."),
                "sources": sources,
                "success": True,
                "mode": mode,
                "language": language,
                "from_cache": False
            }
            
            # Cache result
            if use_cache:
                self.cache.set(query, mode, selected_sources, search_result)
            
            return search_result
            
        except Exception as e:
            return {
                "answer": f"Search error: {str(e)}",
                "sources": [],
                "success": False,
                "error": str(e)
            }
    
    def get_related_questions(self, query: str) -> List[str]:
        """Generate related questions based on the query"""
        related = []
        
        # Simple related question generation
        if "what" in query.lower():
            related.append(query.replace("what", "how").replace("What", "How"))
            related.append(query.replace("what", "why").replace("What", "Why"))
        elif "how" in query.lower():
            related.append(query.replace("how", "what").replace("How", "What"))
            related.append(query.replace("how", "why").replace("How", "Why"))
        elif "why" in query.lower():
            related.append(query.replace("why", "how").replace("Why", "How"))
            related.append(query.replace("why", "what").replace("Why", "What"))
        
        # Add generic related questions
        if not related:
            related = [
                f"How does {query} work?",
                f"What are the benefits of {query}?",
                f"Recent developments in {query}"
            ]
        
        return related[:3]
    
    def clear_cache(self):
        """Clear the search cache"""
        self.cache.clear()


# Global instance
_engine = None

def get_search_engine() -> NexaSearchEngine:
    """Get or create search engine instance"""
    global _engine
    if _engine is None:
        _engine = NexaSearchEngine()
    return _engine

def run_search(
    query: str, 
    mode: str = "balanced",
    selected_sources: Optional[List[str]] = None,
    language: str = "en",
    use_cache: bool = True,
    stream_callback: Optional[callable] = None
) -> Dict[str, Any]:
    """Main search function with enhanced parameters"""
    engine = get_search_engine()
    return engine.search(query, mode, selected_sources, language, use_cache, stream_callback)

def get_related_questions(query: str) -> List[str]:
    """Get related questions"""
    engine = get_search_engine()
    return engine.get_related_questions(query)

def clear_cache():
    """Clear search cache"""
    engine = get_search_engine()
    engine.clear_cache()
