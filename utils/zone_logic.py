"""
zone logic for the score bar
maps a 0-100 score to one of 4 cases: APPROVE, AT THRESHOLD, HIGH RISK, REJECT

matches the decision rule from the notebook:
  score < threshold        → APPROVE  (low risk)
  score == threshold       → AT THRESHOLD  (borderline)
  threshold < score < 50   → HIGH RISK  (elevated risk)
  score >= 50              → REJECT  (high risk)

note: at threshold and high risk both result in REJECT decision
the distinction is only for displaying a more accurate message
"""

from config.constants import ZONE_APPROVE_MAX, ZONE_HIGH_RISK_MAX


def get_zone(score):
    """
    returns a dict with zone name color emoji and message
    score is 0-100
    """
    # use a small epsilon to detect exact-threshold case
    # since float comparison can be tricky
    epsilon = 0.05

    if score < ZONE_APPROVE_MAX - epsilon:
        return {
            "name": "APPROVE",
            "color": "#10B981",
            "emoji": "🟢",
            "message": "Below threshold, low risk of default",
        }
    elif abs(score - ZONE_APPROVE_MAX) <= epsilon:
        return {
            "name": "AT THRESHOLD",
            "color": "#EAB308",
            "emoji": "🟡",
            "message": "Exactly at the decision boundary, borderline case",
        }
    elif score < ZONE_HIGH_RISK_MAX:
        return {
            "name": "HIGH RISK",
            "color": "#F59E0B",
            "emoji": "🟠",
            "message": "Above threshold, elevated risk of default",
        }
    else:
        return {
            "name": "REJECT",
            "color": "#DC2626",
            "emoji": "🔴",
            "message": "Far above threshold, high risk of default",
        }