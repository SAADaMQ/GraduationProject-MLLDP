"""
preprocessor for user input
takes the 31 raw values from the form (14 form fields + 17 json fields)
applies the same transformations used during training:
  - compute the 7 engineered ratios
  - compute the 3 one-hot derived columns
  - compute the emp_length_was_missing flag
  - clip outliers using saved clip_caps
  - scale continuous columns using saved scaler

returns a single row dataframe with exactly 40 features in the correct order
ready to feed to the model
"""

import pandas as pd
import numpy as np


def compute_engineered_ratios(values):
    """
    compute the 7 ratio features the same way they were computed during training
    formulas come from section 5 phase 2 part B of the notebook
    +1 in denominator prevents division by zero (same as training)
    """
    annual_inc = values["annual_inc"]
    installment = values["installment"]
    loan_amnt = values["loan_amnt"]
    revol_bal = values["revol_bal"]
    total_rev_hi_lim = values["total_rev_hi_lim"]
    total_bc_limit = values["total_bc_limit"]

    monthly_income = (annual_inc / 12) + 1

    ratios = {}
    ratios["installment_to_income_ratio"] = installment / monthly_income
    ratios["loan_amnt_to_total_credit"] = loan_amnt / (total_rev_hi_lim + 1)
    ratios["revol_bal_to_income_ratio"] = revol_bal / (annual_inc + 1)
    ratios["debt_to_credit_ratio"] = revol_bal / (total_rev_hi_lim + 1)
    ratios["dti"] = (installment + revol_bal * 0.02) / monthly_income
    ratios["revol_util"] = (revol_bal / (total_rev_hi_lim + 1)) * 100
    ratios["bc_util"] = (revol_bal / (total_bc_limit + 1)) * 100

    return ratios


def compute_onehot(values):
    """
    compute the 3 one-hot columns that the model uses
    we only need 3 specific ones not all categories
    """
    home = values["home_ownership"]
    purpose = values["purpose"]

    onehots = {}
    onehots["home_ownership_RENT"] = 1.0 if home == "RENT" else 0.0
    onehots["home_ownership_MORTGAGE"] = 1.0 if home == "MORTGAGE" else 0.0
    onehots["purpose_small_business"] = 1.0 if purpose == "small_business" else 0.0

    return onehots


def preprocess_input(raw_values, bundle):
    """
    main preprocessing function
    raw_values is a dict with 31 raw values from the form
    bundle is the production_artifacts bundle

    returns a pandas DataFrame with one row and exactly 40 columns
    in the correct order, ready to feed to the model
    """

    # unpack what we need from the bundle
    scaler = bundle["preprocessing"]["scaler"]
    clip_caps = bundle["preprocessing"]["clip_caps"]
    continuous_cols = bundle["preprocessing"]["continuous_cols"]
    final_feature_list = bundle["features"]["final_feature_list"]

    # step 1: compute engineered ratios and one-hots
    ratios = compute_engineered_ratios(raw_values)
    onehots = compute_onehot(raw_values)

    # step 2: emp_length_was_missing flag
    # for manual input we assume user provided a value so flag is 0
    # if they typed nothing, the form would have used default so still 0
    emp_was_missing = 0.0

    # step 3: combine everything into one dict with all 40 features
    all_features = {}

    # copy raw form values (skip categorical text that's now in onehots)
    skip_categorical = ["home_ownership", "purpose"]
    for k, v in raw_values.items():
        if k in skip_categorical:
            continue
        all_features[k] = float(v)

    # add ratios
    for k, v in ratios.items():
        all_features[k] = float(v)

    # add one-hots
    for k, v in onehots.items():
        all_features[k] = float(v)

    # add the missing flag
    all_features["emp_length_was_missing"] = emp_was_missing

    # step 4: apply clip caps (same as training phase 5)
    for col, (lower, upper) in clip_caps.items():
        if col in all_features:
            val = all_features[col]
            if val < lower:
                all_features[col] = lower
            elif val > upper:
                all_features[col] = upper

    # step 5: scale continuous columns using saved scaler
    # the scaler was fit on 63 columns in training but the final model uses 40
    # we need to scale only the columns the scaler knows about

    # build a temporary dataframe with all the columns the scaler expects
    # filling missing ones with 0 (they don't affect the final 40)
    scaler_cols = list(scaler.feature_names_in_)
    temp_row = {}
    for col in scaler_cols:
        if col in all_features:
            temp_row[col] = all_features[col]
        else:
            # column the scaler knows about but we don't have it
            # use 0 since these columns won't be in the final 40 anyway
            temp_row[col] = 0.0

    temp_df = pd.DataFrame([temp_row])[scaler_cols]
    scaled_array = scaler.transform(temp_df)
    scaled_df = pd.DataFrame(scaled_array, columns=scaler_cols)

    # update all_features with the scaled values (only for continuous_cols)
    for col in continuous_cols:
        if col in scaled_df.columns:
            all_features[col] = float(scaled_df[col].iloc[0])

    # step 6: build the final 40-column row in the exact order the model expects
    final_row = {}
    for col in final_feature_list:
        if col in all_features:
            final_row[col] = all_features[col]
        else:
            # this should not happen but handle it gracefully
            final_row[col] = 0.0

    return pd.DataFrame([final_row])[final_feature_list]