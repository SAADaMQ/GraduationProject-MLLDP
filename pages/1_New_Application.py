"""
new application page
4 input modes via tabs: manual form, json paste, file upload, demo cases
all 4 tabs are wired up to the result page
"""

import streamlit as st
import joblib
from config.constants import APP_TITLE, APP_ICON, ARTIFACTS_PATH
from config.theme import GLOBAL_CSS
from forms.manual_form import render_manual_form
from forms.json_paste import render_json_paste
from forms.file_upload import render_file_upload
from forms.demo_cases import render_demo_cases


st.set_page_config(
    page_title=f"{APP_TITLE} - New Application",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


@st.cache_resource
def load_artifacts():
    return joblib.load(ARTIFACTS_PATH)


bundle = load_artifacts()


# page header
st.title("📋 New Loan Application")
st.caption("Assess a loan applicant by providing their financial details")

st.divider()


# helper to send any result to the result page
def go_to_result(payload):
    """payload is either a raw dict (31 fields) or a demo dict {is_demo: True, demo: ...}"""
    if isinstance(payload, dict) and payload.get("is_demo"):
        st.session_state["demo_case"] = payload["demo"]
        # clear raw values so result page knows we came via demo
        if "applicant_raw_values" in st.session_state:
            del st.session_state["applicant_raw_values"]
    else:
        st.session_state["applicant_raw_values"] = payload
        # clear demo if previously set
        if "demo_case" in st.session_state:
            del st.session_state["demo_case"]

    st.switch_page("pages/4_Result.py")


# 4 input mode tabs
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "✍️ Manual Entry",
        "📋 Paste JSON",
        "📁 Upload File",
        "🎯 Demo Cases",
    ]
)

with tab1:
    result = render_manual_form(bundle)
    if result is not None:
        go_to_result(result)

with tab2:
    result = render_json_paste(bundle)
    if result is not None:
        go_to_result(result)

with tab3:
    result = render_file_upload(bundle)
    if result is not None:
        go_to_result(result)

with tab4:
    result = render_demo_cases(bundle)
    if result is not None:
        go_to_result(result)