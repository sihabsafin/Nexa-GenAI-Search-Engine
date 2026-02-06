import os
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import (
    DuckDuckGoSearchRun,
    WikipediaQueryRun,
    ArxivQueryRun
)
from langchain_community.utilities import (
    WikipediaAPIWrapper,
    ArxivAPIWrapper
)

# --- Validate API key ---
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not set in environment")

# --- LLM ---
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="Llama3-8b-8192",
    temperature=0.2
)

# --- Tools ---
search_tool = DuckDuckGoSearchRun(name="Web Search")

wiki_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(
        top_k_results=1,
        doc_content_chars_max=300
    )
)

arxiv_tool = ArxivQueryRun(
    api_wrapper=ArxivAPIWrapper(
        top_k_results=1,
        doc_content_chars_max=300
    )
)

tools = [search_tool, wiki_tool, arxiv_tool]

# --- Agent ---
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

def run_search_agent(query: str) -> str:
    return agent.run(query)
