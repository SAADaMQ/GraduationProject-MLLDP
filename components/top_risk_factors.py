"""
top risk factors component
shows the top features pushing the score up or down

uses shap values:
  positive shap means feature increases risk
  negative shap means feature decreases risk
"""

import streamlit as st
import numpy as np
from utils.feature_labels import get_friendly_label


def render_top_risk_factors(shap_result, top_n=7):
    """
    render the top N most influential features as a clean list
    """
    shap_values = shap_result["shap_values"]
    feature_names = shap_result["feature_names"]

    # rank features by absolute shap value
    abs_shap = np.abs(shap_values)
    top_idx = np.argsort(abs_shap)[::-1][:top_n]

    # render each row as a streamlit container with columns
    for i in top_idx:
        shap_val = float(shap_values[i])
        feature_name = feature_names[i]
        friendly_name = get_friendly_label(feature_name)

        is_risk = shap_val > 0
        pct_impact = abs(shap_val) * 100

        if is_risk:
            icon = "🔴"
            sign = "+"
            color = "#DC2626"
            border_style = "border-left: 4px solid #DC2626;"
        else:
            icon = "🟢"
            sign = "−"
            color = "#10B981"
            border_style = "border-left: 4px solid #10B981;"

        # use a container with custom css for the row card
        row_html = f"""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.8rem 1rem;
            background: white;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            {border_style}
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        ">
            <div>
                <span style="font-size: 1.2rem; margin-right: 0.6rem;">{icon}</span>
                <span style="color: #0A2540; font-weight: 500;">{friendly_name}</span>
            </div>
            <div style="
                font-family: 'Roboto Mono', monospace;
                color: {color};
                font-weight: 700;
                font-size: 1rem;
            ">
                {sign}{pct_impact:.1f}%
            </div>
        </div>
        """
        st.markdown(row_html, unsafe_allow_html=True)

    # legend at the bottom
    st.markdown(
        """
        <div style="
            margin-top: 1rem;
            padding: 0.8rem;
            background: #F3F4F6;
            border-radius: 8px;
            font-size: 0.85rem;
            color: #6B7280;
        ">
            🔴 pushed risk up &nbsp;·&nbsp; 🟢 pulled risk down &nbsp;·&nbsp;
            values in percentage points of default probability
        </div>
        """,
        unsafe_allow_html=True,
    )