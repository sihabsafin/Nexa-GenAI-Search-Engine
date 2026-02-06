"""
Nexa Search - Premium AI Search Engine
Modern UI inspired by Google, Perplexity, and You.com
"""

import streamlit as st
from agent_engine import run_search
from datetime import datetime
import time
from pathlib import Path

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Nexa Search - AI-Powered Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/yourusername/nexa-search',
        'Report a bug': 'https://github.com/yourusername/nexa-search/issues',
        'About': '# Nexa Search\nAI-powered search engine using LangChain & Groq'
    }
)

# ============================================================================
# CUSTOM CSS - PREMIUM DESIGN
# ============================================================================

def load_css():
    """Load custom CSS for premium search engine styling"""
    css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Body */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
        background-attachment: fixed;
    }
    
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 900px;
    }
    
    /* Logo/Header Section */
    .nexa-header {
        text-align: center;
        padding: 2rem 0 3rem 0;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .nexa-logo {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .nexa-tagline {
        color: #8b92b8;
        font-size: 1rem;
        font-weight: 400;
        margin-top: 0.5rem;
    }
    
    /* Search Box Container */
    .search-container {
        position: relative;
        margin: 0 auto 2.5rem auto;
        max-width: 700px;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Search Input Styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 50px !important;
        padding: 1.2rem 3rem 1.2rem 3.5rem !important;
        font-size: 1.05rem !important;
        color: #e8eaf6 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3) !important;
        background: rgba(255, 255, 255, 0.08) !important;
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6b7199 !important;
        font-weight: 400;
    }
    
    /* Search Icon */
    .search-icon {
        position: absolute;
        left: 1.5rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.3rem;
        color: #667eea;
        z-index: 10;
        pointer-events: none;
    }
    
    /* Tool Badges */
    .tools-row {
        display: flex;
        justify-content: center;
        gap: 0.75rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
        animation: fadeIn 1s ease-out 0.3s backwards;
    }
    
    .tool-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: #a5b4fc;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: default;
    }
    
    .tool-badge:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.5);
        transform: translateY(-2px);
    }
    
    .tool-icon {
        font-size: 1rem;
    }
    
    /* Results Container */
    .results-container {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Answer Card */
    .answer-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        animation: slideUp 0.5s ease-out;
    }
    
    .answer-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(102, 126, 234, 0.15);
    }
    
    .answer-icon {
        font-size: 1.5rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .answer-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #e8eaf6;
        margin: 0;
    }
    
    .answer-content {
        color: #c5cae9;
        font-size: 1.05rem;
        line-height: 1.7;
        margin: 0;
    }
    
    /* Sources Section */
    .sources-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(102, 126, 234, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .sources-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #a5b4fc;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .source-item {
        background: rgba(102, 126, 234, 0.08);
        border-left: 3px solid #667eea;
        padding: 0.8rem 1rem;
        margin-bottom: 0.75rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .source-item:hover {
        background: rgba(102, 126, 234, 0.12);
        transform: translateX(5px);
    }
    
    .source-tool {
        font-weight: 600;
        color: #818cf8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .source-query {
        color: #9ca3af;
        font-size: 0.95rem;
        margin-top: 0.3rem;
    }
    
    /* Loading Animation */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Suggestion Pills */
    .suggestions {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 2rem;
        animation: fadeIn 1.2s ease-out 0.5s backwards;
    }
    
    .suggestion-pill {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(102, 126, 234, 0.2);
        color: #9ca3af;
        padding: 0.6rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .suggestion-pill:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: rgba(102, 126, 234, 0.4);
        color: #c5cae9;
        transform: translateY(-2px);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Error Message */
    .stAlert {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
        color: #fca5a5 !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #6b7199;
        font-size: 0.85rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .footer a {
        color: #818cf8;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    .footer a:hover {
        color: #a5b4fc;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .nexa-logo {
            font-size: 2.5rem;
        }
        
        .stTextInput > div > div > input {
            padding: 1rem 2.5rem 1rem 3rem !important;
            font-size: 1rem !important;
        }
        
        .answer-card {
            padding: 1.5rem;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'search_history' not in st.session_state:
    st.session_state.search_history = []

if 'current_result' not in st.session_state:
    st.session_state.current_result = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def add_to_history(query: str, result: dict):
    """Add search to history"""
    st.session_state.search_history.insert(0, {
        'query': query,
        'result': result,
        'timestamp': datetime.now()
    })
    # Keep only last 10 searches
    if len(st.session_state.search_history) > 10:
        st.session_state.search_history = st.session_state.search_history[:10]

def render_answer_card(result: dict):
    """Render the AI answer in a beautiful card"""
    st.markdown("""
    <div class="answer-card">
        <div class="answer-header">
            <div class="answer-icon">✨</div>
            <h2 class="answer-title">AI Answer</h2>
        </div>
        <div class="answer-content">
    """, unsafe_allow_html=True)
    
    st.markdown(result['answer'])
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_sources(sources: list):
    """Render source citations"""
    if not sources:
        return
    
    st.markdown("""
    <div class="sources-card">
        <div class="sources-header">
            <span>🔗</span> Sources Used
        </div>
    """, unsafe_allow_html=True)
    
    for idx, source in enumerate(sources, 1):
        tool = source.get('tool', 'Unknown')
        query = source.get('query', '')
        
        # Map tool names to friendly names
        tool_names = {
            'web_search': '🌐 Web Search',
            'wikipedia': '📚 Wikipedia',
            'arxiv_search': '📄 arXiv',
        }
        
        friendly_tool = tool_names.get(tool, tool)
        
        st.markdown(f"""
        <div class="source-item">
            <div class="source-tool">{friendly_tool}</div>
            <div class="source-query">{query}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Load CSS
    load_css()
    
    # Header
    st.markdown("""
    <div class="nexa-header">
        <div class="nexa-logo">🔍 Nexa Search</div>
        <div class="nexa-tagline">AI-Powered Search • Powered by LangChain & Groq</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Search Container
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Search Input
    query = st.text_input(
        "search",
        placeholder="Ask anything... Try: 'Latest AI developments' or 'Explain quantum computing'",
        label_visibility="collapsed",
        key="search_input"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tool Badges
    st.markdown("""
    <div class="tools-row">
        <div class="tool-badge">
            <span class="tool-icon">🌐</span>
            <span>Web Search</span>
        </div>
        <div class="tool-badge">
            <span class="tool-icon">📚</span>
            <span>Wikipedia</span>
        </div>
        <div class="tool-badge">
            <span class="tool-icon">📄</span>
            <span>arXiv Papers</span>
        </div>
        <div class="tool-badge">
            <span class="tool-icon">🤖</span>
            <span>AI Reasoning</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Execute Search
    if query:
        with st.spinner("🔍 Searching intelligently..."):
            try:
                # Add small delay for better UX
                time.sleep(0.3)
                
                # Run search
                result = run_search(query)
                
                if result['success']:
                    # Store result
                    st.session_state.current_result = result
                    add_to_history(query, result)
                    
                    # Display results
                    st.markdown('<div class="results-container">', unsafe_allow_html=True)
                    render_answer_card(result)
                    render_sources(result.get('sources', []))
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                else:
                    st.error("⚠️ " + result.get('answer', 'Search failed. Please try again.'))
                    
            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")
                st.caption("Please check your API key and try again.")
    
    else:
        # Show example queries when no search
        st.markdown("""
        <div class="suggestions">
            <div class="suggestion-pill">💡 Latest developments in AI</div>
            <div class="suggestion-pill">🔬 Quantum computing explained</div>
            <div class="suggestion-pill">🌍 Climate change research</div>
            <div class="suggestion-pill">🚀 SpaceX recent launches</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        Built with ❤️ using <a href="https://langchain.com" target="_blank">LangChain</a> 
        & <a href="https://groq.com" target="_blank">Groq</a>
        <br>
        <small>Powered by Llama 3.1 70B • Open Source • Privacy Focused</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
