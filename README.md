# MLLDP — Machine Learning Loan Default Predictor

An end-to-end machine learning system that predicts whether a loan application will Default or Not Default, and explains every prediction it makes.

Live App: https://mlldp-app.streamlit.app/

## Overview

MLLDP is a graduation project that takes a loan applicant's financial profile and returns a calibrated default-risk score, a clear approve or reject decision, the reasons behind that decision, and similar past borrowers for context. The goal is not just an accurate model, but a transparent one that a loan officer can actually trust and act on.

The system is built on the LendingClub dataset covering 2007 to 2018, and follows a strict, leak-free methodology. The data is split before any statistic is computed, no synthetic data is used, and all post-decision features are removed so the model only sees what is known at the moment of application.

## Key Features

The application gives the loan officer a calibrated probability of default rather than just a raw model output. Instead of a hard binary verdict, it maps that probability onto a four-zone decision: Approve, Review, High Risk, and Reject. Every prediction is broken down feature by feature using SHAP, so the officer can see exactly what pushed the risk up or down. Alongside the explanation, the app surfaces the ten closest historical borrowers and their real outcomes, giving the decision a layer of real-world context. Data can be entered in four ways: a manual form, pasted JSON, an uploaded file, or a set of ready-made demo cases.

## Final Model

The final model is a calibrated XGBoost classifier with a decision threshold of 0.17. On the held-out test set it achieves a recall of 76.1 percent, a precision of 30.3 percent, an F2 score of 0.585, and an AUC of 0.731.

The model is recall-first by design. In lending, missing a real defaulter costs far more than rejecting a safe applicant, so the project optimizes the F2 score, which weights recall more heavily than precision, rather than chasing raw accuracy.

## Tech Stack

The project is built entirely in Python. It uses Streamlit for the web interface, scikit-learn, XGBoost, and LightGBM for modeling, SHAP for explainability, and Pandas, NumPy, and Matplotlib for data handling and visualization.

## Running Locally

The project requires Python 3.10 or newer. To run it on your machine, clone the repository and move into its folder, optionally create and activate a virtual environment, install the dependencies with pip install -r requirements.txt, and then start the app with streamlit run app.py. Once it launches, the app opens in your browser at http://localhost:8501.

## How It Works

The loan officer enters fourteen application fields and uploads a seventeen-field credit-bureau file, for thirty-one raw values in total. The application then computes seven engineered ratios and the required encoded columns, applies the saved outlier caps and scaler, and produces the forty features the model expects. The calibrated XGBoost model returns a default probability, which is mapped to a score from zero to one hundred and a final decision. SHAP then breaks that prediction into per-feature contributions, and a nearest-neighbour search retrieves the ten most similar past borrowers from a pool of one hundred thousand applicants. Finally, everything is displayed together: the decision banner, the score bar, the top risk factors, the full SHAP breakdown, and the similar borrowers.

## The Training Notebook

The complete machine learning pipeline lives in the notebook folder. It covers data cleaning, feature engineering, the sixty-twenty-twenty split, outlier handling, model tuning with Optuna, probability calibration, threshold selection, and the SHAP setup. Running it from start to finish reproduces the production artifacts bundle, the single file that powers this application.

## Team

This project was developed by Group M14 at the College of Computer and Information Sciences, Imam Mohammad Ibn Saud Islamic University. The team members are Thamer Ahmed Alshamrani, ID 444001747, and Saad Abdurahman Almugrin, ID 443014496. The project was supervised by Dr. Mostafa Ibrahim.

## Notes

This model is trained on US lending data and does not observe post-application life events such as job loss or illness. It is a decision-support tool, not an automated approver. Graduation Project, 2026.
