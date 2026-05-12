"""
MLLDP streamlit app entry point
welcome page is the first thing the user sees
shows logo title and navigation to other pages
"""

import streamlit as st
import joblib
from config.constants import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_ICON,
    ARTIFACTS_PATH,
    LOGO_PATH,
)
from config.theme import GLOBAL_CSS

# page config must be the very first streamlit call
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# inject global css for the whole app
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# load artifacts once cached for the whole session
@st.cache_resource
def load_artifacts():
    """
    load the production bundle from disk
    cached so it loads once per session not per click
    """
    return joblib.load(ARTIFACTS_PATH)


# trigger the load so we know it works
bundle = load_artifacts()


# extra css just for the welcome page
welcome_css = """
<style>
.hero-section {
    text-align: center;
    padding: 4rem 1rem 3rem 1rem;
}
.hero-title {
    font-size: 4rem;
    font-weight: 700;
    color: #0A2540;
    margin: 1rem 0 0.3rem 0;
    letter-spacing: -2px;
}
.hero-subtitle {
    font-size: 1.5rem;
    color: #C9A961;
    font-weight: 500;
    margin: 0;
}
.nav-card {
    background: white;
    border-radius: 16px;
    padding: 2.5rem 1.5rem;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    text-align: center;
    transition: all 250ms ease;
    height: 220px;
    margin-bottom: 1rem;
}
.nav-card:hover {
    border-color: #C9A961;
    box-shadow: 0 8px 24px rgba(10,37,64,0.1);
    transform: translateY(-3px);
}
.nav-icon {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}
.nav-title {
    font-size: 1.4rem;
    font-weight: 600;
    color: #0A2540;
    margin: 0.5rem 0;
}
.nav-description {
    font-size: 0.95rem;
    color: #6B7280;
    line-height: 1.5;
}
.footer-text {
    text-align: center;
    color: #9CA3AF;
    font-size: 0.85rem;
    padding: 3rem 0 1rem 0;
}
</style>
"""
st.markdown(welcome_css, unsafe_allow_html=True)


# hero section with logo and title
col_left, col_center, col_right = st.columns([1, 1, 1])

with col_center:
    # logo centered
    st.image(LOGO_PATH, width=800)

st.markdown(
    f"""
    <div class="hero-section">
        <h1 class="hero-title">{APP_TITLE}</h1>
        <div class="hero-subtitle">{APP_SUBTITLE}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# navigation cards
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="nav-card">
            <div class="nav-icon">📋</div>
            <div class="nav-title">Start Assessment</div>
            <div class="nav-description">
                Evaluate a new loan applicant. Enter details manually,
                paste JSON, upload a file, or try a demo case.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Start Assessment →", key="nav_app", use_container_width=True):
        st.switch_page("pages/1_New_Application.py")

with col2:
    st.markdown(
        """
        <div class="nav-card">
            <div class="nav-icon">📚</div>
            <div class="nav-title">About the Project</div>
            <div class="nav-description">
                Learn about the methodology, the team behind the project,
                and the technologies used to build this system.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Learn More →", key="nav_about", use_container_width=True):
        st.switch_page("pages/3_About.py")


# footer
st.markdown(
    '<div class="footer-text">MLLDP · Imam University CCIS · Graduation Project 2026</div>',
    unsafe_allow_html=True,
)