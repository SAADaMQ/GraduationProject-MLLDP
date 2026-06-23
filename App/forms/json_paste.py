"""
json paste input mode
user pastes a full json with all 31 raw values
useful for testing or for users who have data in another system
"""

import streamlit as st
import json


def render_json_paste(bundle):
    """
    renders a text area for pasting full applicant json
    returns the parsed dict or None if not submitted or invalid
    """

    streamlit_mapping = bundle["features"]["streamlit_mapping"]
    form_field_names = list(streamlit_mapping["form_inputs"].keys())
    json_field_names = streamlit_mapping["json_inputs"]
    all_required = form_field_names + json_field_names

    st.markdown(
        "Paste the full applicant data as JSON below. "
        "It must include all 31 fields (14 application + 17 credit bureau)."
    )

    # example skeleton for the user to start with
    example_skeleton = {
        "loan_amnt": 12000,
        "int_rate": 12.74,
        "term": 36,
        "installment": 373,
        "purpose": "debt_consolidation",
        "annual_inc": 65000,
        "emp_length": 6,
        "home_ownership": "MORTGAGE",
        "mort_acc": 1,
        "num_actv_bc_tl": 3,
        "total_bc_limit": 15100,
        "num_bc_sats": 4,
        "num_rev_accts": 13,
        "num_il_tl": 7,
        "fico_avg": 700,
        "revol_bal": 5000,
        "total_rev_hi_lim": 25000,
        "delinq_2yrs": 0,
        "total_acc": 20,
        "num_actv_rev_tl": 4,
        "acc_open_past_24mths": 4,
        "credit_history_months": 200,
        "mo_sin_old_rev_tl_op": 180,
        "num_tl_op_past_12m": 2,
        "mo_sin_rcnt_tl": 5,
        "bc_open_to_buy": 8000,
        "mths_since_recent_bc": 10,
        "mths_since_recent_inq": 3,
        "percent_bc_gt_75": 25,
        "avg_cur_bal": 5000,
        "mo_sin_old_il_acct": 130,
    }

    # initial value for the text area
    default_text = json.dumps(example_skeleton, indent=2)

    pasted = st.text_area(
        "JSON input",
        value=default_text,
        height=400,
        key="json_paste_area",
    )

    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        submitted = st.button(
            "🔍 Predict Risk",
            type="primary",
            use_container_width=True,
            key="submit_json_paste",
        )

    if not submitted:
        return None

    # parse the json
    try:
        parsed = json.loads(pasted)
    except Exception as e:
        st.error(f"Invalid JSON: {e}")
        return None

    # check all required fields are present
    missing = [f for f in all_required if f not in parsed]
    if missing:
        st.error(
            f"JSON is missing {len(missing)} required fields. "
            f"First few: {', '.join(missing[:5])}"
        )
        return None

    return parsed