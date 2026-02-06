"""
Nexa Search - Premium AI Search Engine (Enhanced)
Features: History, Export, Filters, Streaming, Multi-language, Mobile-responsive
"""

import streamlit as st
from agent_engine import (
    run_search, 
    get_related_questions, 
    clear_cache,
    NexaSearchEngine
)
from datetime import datetime
import time
import json
import io
from pathlib import Path

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Nexa Search - AI-Powered Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/nexa-search',
        'Report a bug': 'https://github.com/yourusername/nexa-search/issues',
        'About': '# Nexa Search\nAI-powered search engine using LangChain & Groq'
    }
)

# ============================================================================
# CUSTOM CSS - ENHANCED PREMIUM DESIGN
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
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1000px;
    }
    
    /* Logo/Header Section */
    .nexa-header {
        text-align: center;
        padding: 1.5rem 0 2.5rem 0;
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
        margin: 0 auto 2rem auto;
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
        justify-content: space-between;
        margin-bottom: 1.2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(102, 126, 234, 0.15);
    }
    
    .answer-title-section {
        display: flex;
        align-items: center;
        gap: 0.75rem;
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
    
    .answer-actions {
        display: flex;
        gap: 0.5rem;
    }
    
    .action-btn {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: #a5b4fc;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .action-btn:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
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
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1328 0%, #1a1f3a 100%);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Checkbox & Radio */
    .stCheckbox, .stRadio {
        color: #c5cae9 !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: #e8eaf6;
    }
    
    /* Suggestions */
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
    
    /* Success Message */
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 12px !important;
        color: #86efac !important;
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
        
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize session state variables"""
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    
    if 'current_result' not in st.session_state:
        st.session_state.current_result = None
    
    if 'feedback' not in st.session_state:
        st.session_state.feedback = {}
    
    if 'search_mode' not in st.session_state:
        st.session_state.search_mode = "balanced"
    
    if 'selected_sources' not in st.session_state:
        st.session_state.selected_sources = ["web_search", "wikipedia", "arxiv_search"]
    
    if 'language' not in st.session_state:
        st.session_state.language = "en"
    
    if 'streaming_enabled' not in st.session_state:
        st.session_state.streaming_enabled = True

init_session_state()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def add_to_history(query: str, result: dict):
    """Add search to history"""
    history_item = {
        'query': query,
        'result': result,
        'timestamp': datetime.now(),
        'mode': result.get('mode', 'balanced'),
        'language': result.get('language', 'en')
    }
    
    # Remove duplicate if exists
    st.session_state.search_history = [
        h for h in st.session_state.search_history 
        if h['query'] != query
    ]
    
    st.session_state.search_history.insert(0, history_item)
    
    # Keep only last 50 searches
    if len(st.session_state.search_history) > 50:
        st.session_state.search_history = st.session_state.search_history[:50]

def export_to_txt(result: dict, query: str) -> str:
    """Export result to TXT format"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    txt_content = f"""
NEXA SEARCH RESULT
{'='*60}

Query: {query}
Timestamp: {timestamp}
Mode: {result.get('mode', 'N/A')}
Language: {result.get('language', 'en')}

ANSWER:
{'-'*60}
{result['answer']}

SOURCES USED:
{'-'*60}
"""
    
    for idx, source in enumerate(result.get('sources', []), 1):
        txt_content += f"{idx}. {source.get('tool', 'Unknown')}: {source.get('query', '')}\n"
    
    txt_content += f"\n{'='*60}\nGenerated by Nexa Search\n"
    
    return txt_content

def export_to_json(result: dict, query: str) -> str:
    """Export result to JSON format"""
    export_data = {
        "query": query,
        "timestamp": datetime.now().isoformat(),
        "result": result
    }
    return json.dumps(export_data, indent=2)

def render_answer_card(result: dict, query: str):
    """Render the AI answer with actions"""
    
    # Answer card HTML
    st.markdown("""
    <div class="answer-card">
        <div class="answer-header">
            <div class="answer-title-section">
                <div class="answer-icon">✨</div>
                <h2 class="answer-title">AI Answer</h2>
            </div>
        </div>
        <div class="answer-content">
    """, unsafe_allow_html=True)
    
    # Display answer
    answer_text = result['answer']
    if result.get('from_cache'):
        st.info("⚡ Loaded from cache (faster response)")
    
    st.markdown(answer_text)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Action buttons row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🔄 Regenerate", key=f"regen_{hash(query)}"):
            with st.spinner("Regenerating..."):
                new_result = run_search(
                    query, 
                    mode=st.session_state.search_mode,
                    selected_sources=st.session_state.selected_sources,
                    language=st.session_state.language,
                    use_cache=False
                )
                st.session_state.current_result = new_result
                st.rerun()
    
    with col2:
        if st.button("👍 Like", key=f"like_{hash(query)}"):
            st.session_state.feedback[query] = "positive"
            st.success("Thanks for your feedback!")
    
    with col3:
        if st.button("👎 Dislike", key=f"dislike_{hash(query)}"):
            st.session_state.feedback[query] = "negative"
            st.info("Feedback noted. We'll improve!")
    
    with col4:
        is_favorited = any(f['query'] == query for f in st.session_state.favorites)
        if st.button("⭐ Favorite" if not is_favorited else "★ Favorited", key=f"fav_{hash(query)}"):
            if not is_favorited:
                st.session_state.favorites.append({
                    'query': query,
                    'result': result,
                    'timestamp': datetime.now()
                })
                st.success("Added to favorites!")
            else:
                st.session_state.favorites = [
                    f for f in st.session_state.favorites if f['query'] != query
                ]
                st.info("Removed from favorites")
            st.rerun()
    
    with col5:
        # Export dropdown
        export_option = st.selectbox(
            "Export",
            ["Select...", "📄 TXT", "📋 JSON", "📑 Copy"],
            key=f"export_{hash(query)}",
            label_visibility="collapsed"
        )
        
        if export_option == "📄 TXT":
            txt_content = export_to_txt(result, query)
            st.download_button(
                label="Download TXT",
                data=txt_content,
                file_name=f"nexa_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key=f"dl_txt_{hash(query)}"
            )
        
        elif export_option == "📋 JSON":
            json_content = export_to_json(result, query)
            st.download_button(
                label="Download JSON",
                data=json_content,
                file_name=f"nexa_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key=f"dl_json_{hash(query)}"
            )
        
        elif export_option == "📑 Copy":
            st.code(result['answer'], language=None)
            st.caption("Select and copy the text above")

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

def render_related_questions(query: str):
    """Render related questions"""
    related = get_related_questions(query)
    
    if related:
        st.markdown("### 🤔 Related Questions")
        cols = st.columns(len(related))
        for idx, (col, question) in enumerate(zip(cols, related)):
            with col:
                if st.button(question, key=f"related_{idx}_{hash(question)}", use_container_width=True):
                    st.session_state.search_input = question
                    st.rerun()

def render_sidebar():
    """Render enhanced sidebar with settings"""
    with st.sidebar:
        st.markdown("## ⚙️ Search Settings")
        
        # Search Mode
        st.markdown("### 🎯 Search Mode")
        mode = st.radio(
            "Mode",
            ["quick", "balanced", "deep"],
            index=["quick", "balanced", "deep"].index(st.session_state.search_mode),
            format_func=lambda x: {
                "quick": "⚡ Quick - Fast answers",
                "balanced": "⚖️ Balanced - Good detail",
                "deep": "🔬 Deep - Comprehensive"
            }[x],
            label_visibility="collapsed"
        )
        st.session_state.search_mode = mode
        
        st.markdown("---")
        
        # Source Selection
        st.markdown("### 📚 Search Sources")
        sources = {
            "web_search": "🌐 Web Search",
            "wikipedia": "📚 Wikipedia",
            "arxiv_search": "📄 arXiv Papers"
        }
        
        selected = []
        for source_id, source_name in sources.items():
            if st.checkbox(
                source_name, 
                value=source_id in st.session_state.selected_sources,
                key=f"source_{source_id}"
            ):
                selected.append(source_id)
        
        st.session_state.selected_sources = selected if selected else list(sources.keys())
        
        st.markdown("---")
        
        # Language Selection
        st.markdown("### 🌍 Language")
        languages = {
            'en': '🇺🇸 English',
            'es': '🇪🇸 Spanish',
            'fr': '🇫🇷 French',
            'de': '🇩🇪 German',
            'it': '🇮🇹 Italian',
            'pt': '🇵🇹 Portuguese',
            'zh': '🇨🇳 Chinese',
            'ja': '🇯🇵 Japanese',
            'ko': '🇰🇷 Korean',
            'ar': '🇸🇦 Arabic'
        }
        
        st.session_state.language = st.selectbox(
            "Response Language",
            list(languages.keys()),
            format_func=lambda x: languages[x],
            index=list(languages.keys()).index(st.session_state.language),
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Performance Settings
        st.markdown("### ⚡ Performance")
        st.session_state.streaming_enabled = st.checkbox(
            "🎬 Enable Streaming",
            value=st.session_state.streaming_enabled
        )
        
        if st.button("🗑️ Clear Cache", use_container_width=True):
            clear_cache()
            st.success("Cache cleared!")
        
        st.markdown("---")
        
        # Search History
        st.markdown("### 📜 Search History")
        if st.session_state.search_history:
            history_option = st.selectbox(
                "Recent Searches",
                ["Select..."] + [h['query'][:50] for h in st.session_state.search_history[:10]],
                label_visibility="collapsed"
            )
            
            if history_option != "Select...":
                # Find the full query
                for h in st.session_state.search_history:
                    if h['query'][:50] == history_option:
                        if st.button("🔍 Search Again", use_container_width=True):
                            st.session_state.search_input = h['query']
                            st.rerun()
                        break
            
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.search_history = []
                st.success("History cleared!")
                st.rerun()
        else:
            st.info("No search history yet")
        
        st.markdown("---")
        
        # Favorites
        st.markdown("### ⭐ Favorites")
        if st.session_state.favorites:
            fav_option = st.selectbox(
                "Saved Searches",
                ["Select..."] + [f['query'][:50] for f in st.session_state.favorites[:10]],
                label_visibility="collapsed",
                key="fav_select"
            )
            
            if fav_option != "Select...":
                for f in st.session_state.favorites:
                    if f['query'][:50] == fav_option:
                        if st.button("🔍 Load Favorite", use_container_width=True):
                            st.session_state.search_input = f['query']
                            st.session_state.current_result = f['result']
                            st.rerun()
                        break
        else:
            st.info("No favorites yet")

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Load CSS
    load_css()
    
    # Render sidebar
    render_sidebar()
    
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
        key="search_input" if "search_input" not in st.session_state else None,
        value=st.session_state.get("search_input", "")
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tool Badges
    mode_badges = {
        "quick": "⚡ Quick Mode",
        "balanced": "⚖️ Balanced Mode",
        "deep": "🔬 Deep Mode"
    }
    
    active_sources = [
        s for s in ["web_search", "wikipedia", "arxiv_search"] 
        if s in st.session_state.selected_sources
    ]
    
    source_icons = {
        "web_search": "🌐",
        "wikipedia": "📚",
        "arxiv_search": "📄"
    }
    
    st.markdown(f"""
    <div class="tools-row">
        <div class="tool-badge">
            <span class="tool-icon">{mode_badges[st.session_state.search_mode]}</span>
        </div>
        {"".join([f'<div class="tool-badge"><span class="tool-icon">{source_icons.get(s, "🔍")}</span></div>' for s in active_sources])}
        <div class="tool-badge">
            <span class="tool-icon">🤖 AI Reasoning</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Execute Search
    if query:
        # Check if we need to run a new search or display cached result
        should_search = True
        if st.session_state.current_result and 'query' in st.session_state:
            if st.session_state.get('last_query') == query:
                should_search = False
        
        if should_search:
            # Create placeholder for streaming
            if st.session_state.streaming_enabled:
                stream_placeholder = st.empty()
                stream_content = ""
                
                def stream_callback(token):
                    nonlocal stream_content
                    stream_content += token
                    stream_placeholder.markdown(stream_content)
                
                with st.spinner("🔍 Searching intelligently..."):
                    result = run_search(
                        query,
                        mode=st.session_state.search_mode,
                        selected_sources=st.session_state.selected_sources,
                        language=st.session_state.language,
                        use_cache=True,
                        stream_callback=stream_callback if st.session_state.streaming_enabled else None
                    )
                
                stream_placeholder.empty()
            else:
                with st.spinner("🔍 Searching intelligently..."):
                    result = run_search(
                        query,
                        mode=st.session_state.search_mode,
                        selected_sources=st.session_state.selected_sources,
                        language=st.session_state.language,
                        use_cache=True
                    )
            
            st.session_state.current_result = result
            st.session_state.last_query = query
            
            if result['success']:
                add_to_history(query, result)
        else:
            result = st.session_state.current_result
        
        # Display results
        if result['success']:
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            render_answer_card(result, query)
            render_sources(result.get('sources', []))
            render_related_questions(query)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error(f"⚠️ {result.get('answer', 'Search failed. Please try again.')}")
            st.caption("Try adjusting your search settings or rephrasing your query.")
    
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
        <small>Powered by Llama 3.3 70B • Open Source • Privacy Focused</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
