# Nexa Search — AI-Powered Search Engine

Nexa Search is a next-generation search engine that combines traditional web search with AI reasoning capabilities. Built on LangChain's agentic framework and powered by Groq's lightning-fast LLM inference, it delivers intelligent, context-aware answers by orchestrating multiple search tools in real-time.

## What Makes Nexa Different?

Traditional search engines return links. Nexa Search understands your question, reasons about the best sources to consult, and synthesizes information from multiple channels — web results, academic papers, and encyclopedic knowledge — into coherent, cited answers.

The agent doesn't just search; it thinks. It decides when to pull from Wikipedia for quick facts, when to dive into arXiv for research papers, and when to scour the web for current events. All of this happens transparently, so you see exactly how it arrives at each answer.

## Core Features

**Intelligent Agent Architecture**  
LangChain's ReAct agent framework enables multi-step reasoning. The system breaks down complex queries, chooses appropriate tools, and iterates until it finds satisfying answers.

**Multi-Source Search**  
- **Web Search**: Real-time results via DuckDuckGo (privacy-focused, no tracking)
- **Wikipedia**: Instant access to verified encyclopedic knowledge
- **arXiv**: Direct queries to 2M+ academic papers in physics, math, CS, and more

**Groq-Powered Inference**  
Uses Groq's LPU™ inference engine with LLaMA-3 models for near-instant response times. What typically takes seconds elsewhere happens in milliseconds here.

**Clean, Familiar Interface**  
A search-engine-inspired UI built with Streamlit. No clutter, no distractions — just a search bar and intelligent results.

## Technology Stack

- **LangChain** — Agent orchestration and tool integration
- **Groq** — Ultra-fast LLM inference with LLaMA-3-70B
- **DuckDuckGo Search API** — Privacy-respecting web search
- **Wikipedia API** — Structured knowledge retrieval
- **arXiv API** — Academic paper search and summaries
- **Streamlit** — Lightweight web framework for the UI

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Groq API key ([get one here](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/nexa-search.git
cd nexa-search
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your API key**

Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=your_api_key_here
```

Or set it as an environment variable:
```bash
export GROQ_API_KEY=your_api_key_here
```

4. **Launch the app**
```bash
streamlit run app.py
```

The interface will open at `http://localhost:8501`

## How It Works

When you enter a query, here's what happens under the hood:

1. **Query Analysis**: The LLM examines your question and formulates a search strategy
2. **Tool Selection**: Based on the query type, it chooses relevant tools (web, Wikipedia, arXiv, or a combination)
3. **Information Gathering**: The agent executes searches and retrieves data from selected sources
4. **Synthesis**: Results are analyzed, cross-referenced, and compiled into a coherent response
5. **Presentation**: You get a clear answer with source attribution

The entire process is transparent — you can see the agent's reasoning chain and which tools it used.

## Example Queries

Try asking:
- "What are the latest developments in quantum computing?"
- "Explain the Riemann hypothesis in simple terms"
- "Recent papers on transformer architecture improvements"
- "How does photosynthesis work at the molecular level?"

## Project Structure

```
nexa-search/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # You are here
└── .env                  # API keys (create this)
```

## Contributing

This project is open source because good tools should be accessible to everyone. If you find bugs, have feature ideas, or want to improve the codebase:

- Open an issue to discuss changes
- Fork the repo and submit a pull request
- Check existing issues before opening new ones

## Why Open Source?

Search should be transparent, not a black box. By keeping this project open, anyone can audit how queries are processed, understand the reasoning mechanisms, and build upon or modify the system for their own needs.

## Limitations

- Requires a Groq API key (free tier available)
- Search quality depends on source availability and LLM reasoning
- arXiv queries are limited to domains covered by the repository
- No result caching yet (every query hits the APIs fresh)

## License

MIT License — use it, modify it, learn from it.

## Acknowledgments

Built with tools from:
- LangChain team for the agent framework
- Groq for blazing-fast inference
- DuckDuckGo for privacy-first search
- The open-source community



