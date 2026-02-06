import streamlit as st
from agent_engine import run_search_agent
from pathlib import Path

# --- Page Config ---
st.set_page_config(
    page_title="Nexa Search",
    page_icon="🔍",
    layout="centered"
)

# --- Load CSS ---
css = Path("assets/style.css")
if css.exists():
    st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)

# --- Header ---
st.markdown("## 🔍 Nexa Search")
st.caption("AI-powered search engine using Tools & Agents")

# --- Search Box ---
with st.container():
    st.markdown("<div class='search-box'>", unsafe_allow_html=True)
    query = st.text_input(
        "",
        placeholder="Search anything… (research, news, concepts)",
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# --- Filters (UX Touch) ---
st.markdown(" ")
st.markdown(
    "<span class='badge'>Web</span>"
    "<span class='badge'>Wikipedia</span>"
    "<span class='badge'>arXiv</span>",
    unsafe_allow_html=True
)

# --- Run Search ---
if query:
    with st.spinner("Searching intelligently…"):
        try:
            result = run_search_agent(query)

            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.markdown("### ✅ AI-Generated Answer")
            st.write(result)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error("Something went wrong. Please try again.")
