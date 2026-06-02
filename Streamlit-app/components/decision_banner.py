"""
decision banner component
big colored banner at the top of the result page
shows the final outcome based on the zone (not the raw decision)

note: the raw decision is binary (APPROVE/REJECT) but the zone gives 4 cases
we use the zone to drive the banner display so AT THRESHOLD shows as REVIEW
instead of a confusing REJECTED with a borderline message
"""

import streamlit as st


def render_decision_banner(prediction_result, zone):
    """
    render the decision banner using the zone classification
    """
    zone_name = zone["name"]
    color = zone["color"]
    zone_message = zone["message"]

    # map zone to banner display
    if zone_name == "APPROVE":
        icon = "✅"
        title_text = "APPROVED"
    elif zone_name == "AT THRESHOLD":
        icon = "⚖️"
        title_text = "REVIEW REQUIRED"
    elif zone_name == "HIGH RISK":
        icon = "⚠️"
        title_text = "REJECTED"
    else:  # REJECT
        icon = "🚫"
        title_text = "REJECTED"

    banner_html = f"""
    <div style="
        background: {color};
        color: white;
        padding: 2rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    ">
        <div style="font-size: 3rem; margin-bottom: 0.3rem;">{icon}</div>
        <div style="font-size: 2.5rem; font-weight: 700; letter-spacing: 2px;">
            {title_text}
        </div>
        <div style="font-size: 1.1rem; opacity: 0.95; margin-top: 0.5rem;">
            Zone: {zone_name} · {zone_message}
        </div>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)