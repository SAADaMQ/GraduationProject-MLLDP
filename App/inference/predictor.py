"""
prediction wrapper
takes preprocessed input and returns probability + decision
"""

from config.constants import DECISION_THRESHOLD


def predict(preprocessed_df, bundle):
    """
    run the model on a single preprocessed row
    returns a dict with probability, score (0-100), decision, threshold
    """
    model = bundle["model"]["hero_model"]
    threshold = bundle["model"]["hero_threshold"]

    # get probability of default (class 1)
    proba = model.predict_proba(preprocessed_df)[0, 1]

    # convert to 0-100 score for display
    score = round(float(proba) * 100, 1)

    # binary decision based on threshold
    decision = "REJECT" if proba >= threshold else "APPROVE"

    return {
        "probability": float(proba),
        "score": score,
        "decision": decision,
        "threshold": float(threshold),
        "threshold_pct": float(threshold) * 100,
    }