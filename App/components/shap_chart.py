"""
shap waterfall chart component
shows the full breakdown of how each feature pushed the prediction
collapsed by default since top risk factors gives the summary
"""

import streamlit as st
import shap
import numpy as np
import matplotlib.pyplot as plt
from utils.feature_labels import get_friendly_label


def render_shap_chart(shap_result):
    """
    render the shap waterfall chart inside an expander
    """
    with st.expander("📉 View Detailed SHAP Waterfall", expanded=False):
        shap_values = shap_result["shap_values"]
        expected_value = shap_result["expected_value"]
        feature_values = shap_result["feature_values"]
        raw_names = shap_result["feature_names"]

        # use friendly labels instead of raw column names
        friendly_names = [get_friendly_label(n) for n in raw_names]

        # build an Explanation object for shap to plot
        explanation = shap.Explanation(
            values=shap_values,
            base_values=expected_value,
            data=np.array(feature_values),
            feature_names=friendly_names,
        )

        # close any old figures to keep memory clean
        plt.close("all")

        # build the figure at a reasonable size
        fig, ax = plt.subplots(figsize=(8, 6))
        shap.waterfall_plot(explanation, max_display=12, show=False)
        plt.tight_layout()

        # constrain the chart width in the page using columns
        col_left, col_mid, col_right = st.columns([1, 4, 1])
        with col_mid:
            st.pyplot(fig, use_container_width=True, clear_figure=True)

        st.caption(
            "This chart shows how each feature contributed to the final probability. "
            "Red bars push the score up (more risky), blue bars push it down (less risky)."
        )