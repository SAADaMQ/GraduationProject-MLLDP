# MLLDP — Machine Learning Loan Default Predictor

An end-to-end machine learning pipeline that predicts whether a loan application will **Default** or **Not Default**, and explains every prediction it makes.

**Live App:** [mlldp-app.streamlit.app](https://mlldp-app.streamlit.app/)

---

## Overview

MLLDP is a graduation project that takes a loan applicant's financial profile and returns a calibrated default-risk score, a clear approve / review / reject decision, the reasons behind that decision, and similar past borrowers for context. The goal is not just an accurate model, but a **transparent** one that a loan officer can actually trust and act on.

The system is built on the LendingClub dataset (2007–2018) and follows a strict, leak-free methodology: the data is split **before** any statistic is computed, no synthetic data is used, and all post-decision features are removed so the model only sees what is known at application time.

---

## Key Features

- **Calibrated risk score** — a real probability of default, not just a raw model output.
- **Four-zone decision** — Approve, Review, High Risk, Reject, instead of a hard binary.
- **SHAP explanations** — every prediction is broken down feature-by-feature.
- **Similar past borrowers** — 10 closest historical applicants and their real outcomes.
- **Four input modes** — manual form, paste JSON, upload file, or try a demo case.

---

## Final Model

| Item | Value |
|------|-------|
| Model | Calibrated XGBoost |
| Decision threshold | 0.17 |
| Recall | 76.1% |
| Precision | 30.3% |
| F2 score | 0.585 |
| AUC | 0.731 |

The model is **recall-first** by design: in lending, missing a real defaulter costs far more than rejecting a safe applicant, so we optimize the F2 score (which weights recall over precision) rather than raw accuracy.

---

## Tech Stack

`Python` · `Streamlit` · `scikit-learn` · `XGBoost` · `LightGBM` · `SHAP` · `Pandas` · `NumPy` · `Matplotlib`

---

## Project Structure

```
MLLDP-Streamlit/
├── app.py                  # entry point — welcome page
├── requirements.txt        # python dependencies
├── artifacts/              # trained model bundle + logo
│   ├── production_artifacts.pkl
│   └── logo.png
├── config/                 # constants and theme
├── forms/                  # 4 input modes (manual, json, upload, demo)
├── inference/              # preprocessing, prediction, SHAP, KNN
├── components/             # visual result components
├── pages/                  # new application, result, about
├── utils/                  # zone logic and feature labels
└── notebook/               # training notebook (full ML pipeline)
```

---

## Running Locally

**Requirements:** Python 3.10 or newer.

```bash
# 1. clone the repository
git clone https://github.com/SAADaMQ/MLLDP-Streamlit.git
cd MLLDP-Streamlit

# 2. (optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# 3. install dependencies
pip install -r requirements.txt

# 4. run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## How It Works

1. **Input** — the loan officer enters 14 application fields and uploads a 17-field credit-bureau JSON (31 raw values total).
2. **Preprocessing** — the app computes 7 engineered ratios and the required one-hot columns, applies the saved clip caps and scaler, producing the 40 features the model expects.
3. **Prediction** — the calibrated XGBoost model returns a default probability, mapped to a 0–100 score and a decision.
4. **Explanation** — SHAP breaks the prediction into per-feature contributions, and a KNN search surfaces the 10 most similar past borrowers from a 100k-applicant pool.
5. **Result** — everything is displayed: decision banner, score bar, top risk factors, full SHAP waterfall, and the similar borrowers table.

---

## The Training Notebook

The full machine learning pipeline — data cleaning, feature engineering, the 60/20/20 split, outlier handling, model tuning with Optuna, probability calibration, threshold selection, and SHAP setup — lives in `notebook/`. Running it end-to-end reproduces `production_artifacts.pkl`, the single bundle that powers this app.

---

## Team

**Group M14** — College of Computer and Information Sciences, Imam Mohammad Ibn Saud Islamic University

- Thamer Ahmed Alshamrani — 444001747
- Saad Abdurahman Almugrin — 443014496

**Supervisor:** Dr. Mostafa Ibrahim

---

## Notes

- This model is trained on US lending data and does not observe post-application life events (job loss, illness). It is a decision-support tool, not an automated approver.
- Graduation Project · 2026
