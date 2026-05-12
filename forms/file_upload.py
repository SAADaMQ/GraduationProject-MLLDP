"""
file upload input mode
user uploads a single json file with all 31 raw values
"""

import streamlit as st
import json


def render_file_upload(bundle):
    """
    renders a file uploader for full applicant json
    returns the parsed dict or None if no file submitted or invalid
    """

    streamlit_mapping = bundle["features"]["streamlit_mapping"]
    form_field_names = list(streamlit_mapping["form_inputs"].keys())
    json_field_names = streamlit_mapping["json_inputs"]
    all_required = form_field_names + json_field_names

    st.markdown(
        "Upload a JSON file containing the full applicant data. "
        "The file must include all 31 fields (14 application + 17 credit bureau)."
    )

    uploaded_file = st.file_uploader(
        "Choose a JSON file",
        type=["json"],
        key="full_applicant_json",
    )

    if uploaded_file is None:
        return None

    # try to parse the file
    try:
        parsed = json.loads(uploaded_file.read())
    except Exception as e:
        st.error(f"Could not parse JSON: {e}")
        return None

    # check all required fields are present
    missing = [f for f in all_required if f not in parsed]
    if missing:
        st.error(
            f"File is missing {len(missing)} required fields. "
            f"First few: {', '.join(missing[:5])}"
        )
        return None

    st.success(f"File loaded successfully. Found {len(parsed)} fields.")

    # preview the data
    with st.expander("Preview uploaded data"):
        st.json(parsed)

    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        submitted = st.button(
            "🔍 Predict Risk",
            type="primary",
            use_container_width=True,
            key="submit_file_upload",
        )

    if not submitted:
        return None

    return parsed