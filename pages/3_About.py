"""
about page
project overview, methodology summary, team, and technologies
no performance numbers here per project requirements
"""

import streamlit as st
from config.constants import APP_TITLE, APP_ICON
from config.theme import GLOBAL_CSS


st.set_page_config(
    page_title=f"{APP_TITLE} - About",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# extra css for the about page
about_css = """
<style>
.about-hero {
    text-align: center;
    padding: 2rem 0 1rem 0;
}
.about-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #0A2540;
    margin-bottom: 0.3rem;
}
.about-subtitle {
    font-size: 1.2rem;
    color: #C9A961;
    font-weight: 500;
}
.section-card {
    background: white;
    border-radius: 12px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    border: 1px solid #E5E7EB;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.section-heading {
    color: #0A2540;
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid #C9A961;
}
.section-text {
    color: #374151;
    font-size: 1rem;
    line-height: 1.7;
}
.team-card {
    background: #F9FAFB;
    padding: 1.2rem 1.5rem;
    border-radius: 10px;
    margin-bottom: 0.7rem;
    border-left: 4px solid #C9A961;
}
.team-name {
    color: #0A2540;
    font-weight: 600;
    font-size: 1.05rem;
}
.team-id {
    color: #6B7280;
    font-family: 'Roboto Mono', monospace;
    font-size: 0.85rem;
    margin-top: 0.2rem;
}
.supervisor-card {
    background: #FEF3C7;
    padding: 1.2rem 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #C9A961;
    margin-top: 1rem;
}
.tech-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 0.8rem;
    margin-top: 1rem;
}
.tech-pill {
    background: #F3F4F6;
    color: #0A2540;
    padding: 0.7rem 1rem;
    border-radius: 8px;
    text-align: center;
    font-weight: 500;
    border: 1px solid #E5E7EB;
}
.institution-block {
    text-align: center;
    background: #0A2540;
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin-top: 1rem;
}
.institution-name {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.3rem;
}
.institution-detail {
    font-size: 0.95rem;
    opacity: 0.9;
}
</style>
"""
st.markdown(about_css, unsafe_allow_html=True)


# hero
st.markdown(
    """
    <div class="about-hero">
        <div class="about-title">About MLLDP</div>
        <div class="about-subtitle">Machine Learning Loan Default Predictor</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# section 1: project overview
st.markdown(
    """
    <div class="section-card">
        <div class="section-heading">📋 Project Overview</div>
        <div class="section-text">
            MLLDP is a machine learning system that predicts the probability of a loan
            default at the application stage. Built as a graduation project for the
            College of Computer and Information Sciences at Imam Mohammad Ibn Saud
            Islamic University, the system is trained on real-world lending data and
            designed to support loan officers in their credit risk decisions.
            <br><br>
            Beyond a single binary decision, the system explains why each prediction
            was made and surfaces similar past borrowers, giving loan officers the
            context they need to confidently approve or reject applications.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# section 2: methodology
st.markdown(
    """
    <div class="section-card">
        <div class="section-heading">🔬 Methodology</div>
        <div class="section-text">
            The pipeline processes the LendingClub dataset and engineers key financial features. The final model is a calibrated XGBoost, specifically tuned to prioritize risk detection and catch potential defaulters.
            <br><br>
            Predictions are fully transparent: SHAP values explain the impact of each feature, while a K-nearest-neighbour (KNN) search retrieves similar historical cases for extra context.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# section 3: team
st.markdown(
    """
    <div class="section-card">
        <div class="section-heading">👥 Team</div>
        <div class="team-card">
            <div class="team-name">Thamer Ahmed Alshamrani</div>
            <div class="team-id">ID: 444001747</div>
        </div>
        <div class="team-card">
            <div class="team-name">Saad Abdurahman Almugrin</div>
            <div class="team-id">ID: 443014496</div>
        </div>
        <div class="supervisor-card">
            <div class="team-name">Supervised by Dr. Mostafa Ibrahim</div>
            <div style="color: #92400E; font-size: 0.9rem; margin-top: 0.2rem;">
                Project Supervisor
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# section 4: institution
st.markdown(
    """
    <div class="section-card">
        <div class="section-heading">🏛️ Institution</div>
        <div class="institution-block">
            <div class="institution-name">Imam Mohammad Ibn Saud Islamic University</div>
            <div class="institution-detail">College of Computer and Information Sciences</div>
            <div class="institution-detail">Graduation Project &middot; Group M14 &middot; 2026</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# section 5: technologies
st.markdown(
    """
    <div class="section-card">
        <div class="section-heading">🛠️ Technologies</div>
        <div class="section-text">
            The system is built on a modern open-source Python stack:
        </div>
        <div class="tech-grid">
            <div class="tech-pill">🐍 Python 3.13</div>
            <div class="tech-pill">⚡ Streamlit</div>
            <div class="tech-pill">🌳 XGBoost</div>
            <div class="tech-pill">💡 LightGBM</div>
            <div class="tech-pill">🔬 scikit-learn</div>
            <div class="tech-pill">📊 SHAP</div>
            <div class="tech-pill">🐼 pandas</div>
            <div class="tech-pill">🔢 NumPy</div>
            <div class="tech-pill">📈 matplotlib</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.divider()


# navigation
col_a, col_b = st.columns(2)
with col_a:
    if st.button("← Home", use_container_width=True):
        st.switch_page("app.py")
with col_b:
    if st.button("📋 New Application", use_container_width=True):
        st.switch_page("pages/1_New_Application.py")