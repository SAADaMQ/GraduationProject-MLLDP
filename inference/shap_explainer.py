"""
shap explainer for a single applicant
uses KernelExplainer with the saved background sample
"""

import streamlit as st
import shap
import numpy as np
from config.constants import SHAP_NSAMPLES


@st.cache_resource
def build_explainer(_bundle):
    """
    build the kernel explainer using the saved background sample
    the underscore prefix on _bundle tells streamlit not to hash it
    (cant hash a dict containing a model)
    """
    shap_setup = _bundle["shap"]
    background = shap_setup["background_sample"]
    model = _bundle["model"]["hero_model"]

    def predict_class1(input_data):
        return model.predict_proba(input_data)[:, 1]

    explainer = shap.KernelExplainer(predict_class1, background)
    return explainer


def explain_applicant(preprocessed_df, bundle):
    """
    compute shap values for a single applicant
    returns the shap values array and the expected value
    """
    explainer = build_explainer(bundle)
    expected_value = bundle["shap"]["expected_value"]

    # fix the random seed so shap values are deterministic
    # without this every run gives slightly different results
    np.random.seed(42)

    shap_values = explainer.shap_values(preprocessed_df, nsamples=SHAP_NSAMPLES)

    return {
        "shap_values": shap_values[0],
        "expected_value": expected_value,
        "feature_names": preprocessed_df.columns.tolist(),
        "feature_values": preprocessed_df.iloc[0].values,
    }