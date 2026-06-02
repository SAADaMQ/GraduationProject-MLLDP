"""
manual entry form for loan application
14 form fields for loan officer to type in
17 additional fields uploaded as json (credit bureau data)
returns combined dict of all 31 raw values for the predictor
"""

import streamlit as st
import json


def render_manual_form(bundle):
    """
    render the manual entry form and return user input
    returns None if user hasn't submitted yet
    returns dict of all raw values once submitted
    """

    # get the streamlit feature mapping from the bundle
    streamlit_mapping = bundle["features"]["streamlit_mapping"]
    form_inputs = streamlit_mapping["form_inputs"]
    json_inputs = streamlit_mapping["json_inputs"]

    # storage for collected values
    form_values = {}

    # section 1: loan officer inputs the loan details
    st.subheader("Loan Details")
    st.caption("Information about the requested loan")

    col1, col2 = st.columns(2)

    with col1:
        meta = form_inputs["loan_amnt"]
        form_values["loan_amnt"] = st.number_input(
            meta["label"],
            min_value=float(meta["min"]),
            max_value=float(meta["max"]),
            value=float(meta["default"]),
            step=float(meta["step"]),
            key="loan_amnt",
        )

        meta = form_inputs["int_rate"]
        form_values["int_rate"] = st.number_input(
            meta["label"],
            min_value=float(meta["min"]),
            max_value=float(meta["max"]),
            value=float(meta["default"]),
            step=float(meta["step"]),
            key="int_rate",
        )

        meta = form_inputs["term"]
        form_values["term"] = st.selectbox(
            meta["label"],
            options=meta["options"],
            index=meta["options"].index(meta["default"]),
            key="term",
        )

    with col2:
        meta = form_inputs["installment"]
        form_values["installment"] = st.number_input(
            meta["label"],
            min_value=float(meta["min"]),
            max_value=float(meta["max"]),
            value=float(meta["default"]),
            step=float(meta["step"]),
            key="installment",
        )

        meta = form_inputs["purpose"]
        form_values["purpose"] = st.selectbox(
            meta["label"],
            options=meta["options"],
            index=meta["options"].index(meta["default"]),
            key="purpose",
        )

    st.divider()

    # section 2: applicant personal and financial info
    st.subheader("Applicant Information")
    st.caption("Personal and employment details")

    col1, col2 = st.columns(2)

    with col1:
        meta = form_inputs["annual_inc"]
        form_values["annual_inc"] = st.number_input(
            meta["label"],
            min_value=float(meta["min"]),
            max_value=float(meta["max"]),
            value=float(meta["default"]),
            step=float(meta["step"]),
            key="annual_inc",
        )

        meta = form_inputs["emp_length"]
        form_values["emp_length"] = st.number_input(
            meta["label"],
            min_value=int(meta["min"]),
            max_value=int(meta["max"]),
            value=int(meta["default"]),
            step=int(meta["step"]),
            key="emp_length",
        )

    with col2:
        meta = form_inputs["home_ownership"]
        form_values["home_ownership"] = st.selectbox(
            meta["label"],
            options=meta["options"],
            index=meta["options"].index(meta["default"]),
            key="home_ownership",
        )

        meta = form_inputs["mort_acc"]
        form_values["mort_acc"] = st.number_input(
            meta["label"],
            min_value=int(meta["min"]),
            max_value=int(meta["max"]),
            value=int(meta["default"]),
            step=int(meta["step"]),
            key="mort_acc",
        )

    st.divider()

    # section 3: applicant credit profile
    st.subheader("Credit Profile")
    st.caption("Information about the applicant's existing credit accounts")

    col1, col2 = st.columns(2)

    with col1:
        meta = form_inputs["num_actv_bc_tl"]
        form_values["num_actv_bc_tl"] = st.number_input(
            meta["label"],
            min_value=int(meta["min"]),
            max_value=int(meta["max"]),
            value=int(meta["default"]),
            step=int(meta["step"]),
            key="num_actv_bc_tl",
        )

        meta = form_inputs["total_bc_limit"]
        form_values["total_bc_limit"] = st.number_input(
            meta["label"],
            min_value=float(meta["min"]),
            max_value=float(meta["max"]),
            value=float(meta["default"]),
            step=float(meta["step"]),
            key="total_bc_limit",
        )

        meta = form_inputs["num_bc_sats"]
        form_values["num_bc_sats"] = st.number_input(
            meta["label"],
            min_value=int(meta["min"]),
            max_value=int(meta["max"]),
            value=int(meta["default"]),
            step=int(meta["step"]),
            key="num_bc_sats",
        )

    with col2:
        meta = form_inputs["num_rev_accts"]
        form_values["num_rev_accts"] = st.number_input(
            meta["label"],
            min_value=int(meta["min"]),
            max_value=int(meta["max"]),
            value=int(meta["default"]),
            step=int(meta["step"]),
            key="num_rev_accts",
        )

        meta = form_inputs["num_il_tl"]
        form_values["num_il_tl"] = st.number_input(
            meta["label"],
            min_value=int(meta["min"]),
            max_value=int(meta["max"]),
            value=int(meta["default"]),
            step=int(meta["step"]),
            key="num_il_tl",
        )

    st.divider()

    # section 4: credit bureau json upload
    st.subheader("Credit Bureau Data")
    st.caption(
        "Upload the JSON file with the applicant's credit bureau report "
        "(17 fields like FICO score, revolving balance, account history, etc.)"
    )

    uploaded_file = st.file_uploader(
        "Upload credit bureau JSON",
        type=["json"],
        key="credit_bureau_json",
    )

    json_values = None
    if uploaded_file is not None:
        try:
            json_values = json.loads(uploaded_file.read())
            st.success(f"Loaded {len(json_values)} fields from JSON")

            # quick check that all required fields are present
            missing = [f for f in json_inputs if f not in json_values]
            if missing:
                st.warning(
                    f"JSON is missing {len(missing)} required fields: "
                    f"{', '.join(missing[:5])}..."
                )
                json_values = None
        except Exception as e:
            st.error(f"Could not parse JSON: {e}")
            json_values = None

    st.divider()

    # submit button
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        submitted = st.button(
            "🔍 Predict Risk",
            type="primary",
            use_container_width=True,
            key="submit_manual_form",
        )

    if not submitted:
        return None

    if json_values is None:
        st.error(
            "Please upload the credit bureau JSON file before submitting. "
            "You can find sample JSON files in the project's artifacts folder."
        )
        return None

    # combine form values and json values into one dict
    combined = {**form_values, **json_values}
    return combined