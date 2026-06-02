"""
result dashboard page
handles two input paths:
  1. raw values from form/paste/upload  - runs full preprocessing
  2. demo case from the bundle          - uses saved preprocessed features
"""

import streamlit as st
import pandas as pd
import joblib
from config.constants import APP_TITLE, APP_ICON, ARTIFACTS_PATH
from config.theme import GLOBAL_CSS
from inference.preprocessor import preprocess_input
from inference.predictor import predict
from inference.shap_explainer import explain_applicant
from inference.knn_search import find_similar_borrowers
from utils.zone_logic import get_zone
from components.decision_banner import render_decision_banner
from components.score_bar import render_score_bar
from components.top_risk_factors import render_top_risk_factors
from components.shap_chart import render_shap_chart
from components.similar_borrowers import render_similar_borrowers


st.set_page_config(
    page_title=f"{APP_TITLE} - Result",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


@st.cache_resource
def load_artifacts():
    return joblib.load(ARTIFACTS_PATH)


bundle = load_artifacts()


# check input source: either raw values or a demo case
has_raw_values = "applicant_raw_values" in st.session_state
has_demo_case = "demo_case" in st.session_state

if not has_raw_values and not has_demo_case:
    st.warning("No applicant data found. Please submit an application first.")
    if st.button("← Go to New Application"):
        st.switch_page("pages/1_New_Application.py")
    st.stop()


# header
st.title("📊 Assessment Result")

if has_demo_case:
    demo = st.session_state["demo_case"]
    st.caption(f"Pre-defined demo case: {demo['name']}")
else:
    st.caption("Risk assessment for the submitted loan applicant")

st.divider()


# build the preprocessed dataframe and the prediction
# two paths depending on input source
try:
    final_feature_list = bundle["features"]["final_feature_list"]

    if has_demo_case:
        # demo case has applicant_features already scaled and ready
        demo = st.session_state["demo_case"]
        preprocessed_df = pd.DataFrame([demo["applicant_features"]])[final_feature_list]
    else:
        # raw values from form/paste/upload need full preprocessing
        raw_values = st.session_state["applicant_raw_values"]
        preprocessed_df = preprocess_input(raw_values, bundle)

    prediction_result = predict(preprocessed_df, bundle)

except Exception as e:
    st.error(f"Could not generate prediction: {e}")
    st.exception(e)
    st.stop()


# figure out the zone from the score
zone = get_zone(prediction_result["score"])


# decision banner
render_decision_banner(prediction_result, zone)


# score bar with animation
render_score_bar(prediction_result["score"])

st.markdown("<br>", unsafe_allow_html=True)


# decision details
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Default Probability",
        value=f"{prediction_result['probability']*100:.1f}%",
    )

with col2:
    st.metric(
        label="Decision Threshold",
        value=f"{prediction_result['threshold_pct']:.0f}%",
        help="Above this threshold the model recommends rejection",
    )

with col3:
    st.metric(
        label="Risk Zone",
        value=zone["name"],
    )


st.divider()


# compute shap values and render explanations
with st.spinner("Computing feature explanations..."):
    shap_result = explain_applicant(preprocessed_df, bundle)

st.subheader("📊 Top Risk Factors")
st.caption("The features that influenced this applicant's risk score the most")

render_top_risk_factors(shap_result, top_n=7)

st.markdown("<br>", unsafe_allow_html=True)

render_shap_chart(shap_result)


st.divider()


# similar past borrowers
st.subheader("👥 Similar Past Borrowers")
st.caption("The 10 closest historical applicants based on financial profile")

with st.spinner("Finding similar borrowers..."):
    knn_result = find_similar_borrowers(preprocessed_df, bundle)

render_similar_borrowers(knn_result)


st.divider()


# applicant summary at the bottom (only for raw inputs not demos)
if has_raw_values:
    with st.expander("📋 Applicant Summary"):
        st.json(st.session_state["applicant_raw_values"])
elif has_demo_case:
    demo = st.session_state["demo_case"]
    with st.expander("📋 Demo Case Details"):
        st.markdown(f"**Name:** {demo['name']}")
        st.markdown(f"**Description:** {demo['description']}")
        st.markdown(f"**Expected Probability:** {demo['probability']*100:.2f}%")
        st.markdown(f"**Actual Outcome:** {'Defaulted' if demo['actual_label'] == 1 else 'Paid in full'}")


# bottom navigation
col_a, col_b = st.columns(2)
with col_a:
    if st.button("← New Assessment", use_container_width=True):
        for key in ["applicant_raw_values", "demo_case"]:
            if key in st.session_state:
                del st.session_state[key]
        st.switch_page("pages/1_New_Application.py")

with col_b:
    if st.button("🏠 Home", use_container_width=True):
        for key in ["applicant_raw_values", "demo_case"]:
            if key in st.session_state:
                del st.session_state[key]
        st.switch_page("app.py")