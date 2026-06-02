"""
demo cases input mode
user picks from 5 pre-computed cases stored in the bundle

these cases have applicant_features already preprocessed (scaled)
so we send them directly to the model bypassing the preprocessor
this guarantees the prediction matches what's saved in the bundle
"""

import streamlit as st


def render_demo_cases(bundle):
    """
    renders a selector for the 5 demo cases
    returns a dict with the selected demo or None if not submitted
    """

    demos = bundle["demos"]

    st.markdown(
        "Select one of the pre-defined demo cases below. "
        "Each demo represents a different risk profile from the test set."
    )

    # build display names with expected probability
    options = []
    for i, demo in enumerate(demos):
        proba_pct = demo["probability"] * 100
        outcome = "defaulted" if demo["actual_label"] == 1 else "paid"
        label = f"{demo['name']} ({proba_pct:.1f}% risk, actually {outcome})"
        options.append(label)

    selected_idx = st.selectbox(
        "Choose a demo case",
        options=range(len(options)),
        format_func=lambda i: options[i],
        key="demo_selector",
    )

    # show description for the selected demo
    selected_demo = demos[selected_idx]
    st.info(f"**{selected_demo['name']}** ─ {selected_demo['description']}")

    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        submitted = st.button(
            "🔍 Predict Risk",
            type="primary",
            use_container_width=True,
            key="submit_demo",
        )

    if not submitted:
        return None

    # return the full demo dict so result page can use applicant_features directly
    return {
        "demo": selected_demo,
        "is_demo": True,
    }