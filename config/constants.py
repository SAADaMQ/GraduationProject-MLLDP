"""
central configuration for the streamlit app
all paths and thresholds live here
update once propagates everywhere
"""

import os

# project paths
# __file__ is this constants.py file
# dirname twice gets us to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACTS_PATH = os.path.join(PROJECT_ROOT, "artifacts", "production_artifacts.pkl")
LOGO_PATH = os.path.join(PROJECT_ROOT, "artifacts", "logo.png")

# decision threshold from section 6 of the notebook
DECISION_THRESHOLD = 0.17

# score bar zones (visual only - decision still uses 0.17)
# scale is 0 to 100 we multiply probability by 100
ZONE_APPROVE_MAX = 17     # 0-17 score = approve
ZONE_HIGH_RISK_MAX = 50   # 17-50 score = high risk
# anything above 50 is reject zone

# shap settings
SHAP_NSAMPLES = 2000

# similar borrowers settings
NUM_SIMILAR_BORROWERS = 10

# ui settings
APP_TITLE = "MLLDP"
APP_SUBTITLE = "Loan Default Predictor"
APP_ICON = "💳"