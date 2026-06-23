"""
mapping from raw feature names to human-friendly labels
used in top risk factors text summary
"""

FRIENDLY_LABELS = {
    "int_rate": "Interest Rate",
    "dti": "Debt-to-Income Ratio",
    "installment_to_income_ratio": "Installment-to-Income Ratio",
    "acc_open_past_24mths": "Accounts Opened (24 months)",
    "term": "Loan Term",
    "fico_avg": "FICO Score",
    "loan_amnt": "Loan Amount",
    "mo_sin_old_rev_tl_op": "Oldest Revolving Account Age",
    "num_actv_rev_tl": "Active Revolving Accounts",
    "loan_amnt_to_total_credit": "Loan-to-Credit Ratio",
    "revol_bal_to_income_ratio": "Revolving Balance-to-Income",
    "annual_inc": "Annual Income",
    "credit_history_months": "Credit History Length",
    "mths_since_recent_bc": "Months Since Recent Bankcard",
    "mort_acc": "Mortgage Accounts",
    "emp_length_was_missing": "Employment Info Missing",
    "total_bc_limit": "Total Bankcard Limit",
    "bc_open_to_buy": "Bankcard Available Credit",
    "revol_bal": "Revolving Balance",
    "total_rev_hi_lim": "Total Revolving Limit",
    "emp_length": "Employment Length",
    "bc_util": "Bankcard Utilization",
    "num_il_tl": "Installment Accounts",
    "total_acc": "Total Credit Accounts",
    "mths_since_recent_inq": "Months Since Recent Inquiry",
    "revol_util": "Revolving Utilization",
    "installment": "Monthly Installment",
    "num_rev_accts": "Revolving Accounts",
    "debt_to_credit_ratio": "Debt-to-Credit Ratio",
    "avg_cur_bal": "Average Current Balance",
    "home_ownership_RENT": "Home Ownership (Rent)",
    "delinq_2yrs": "Delinquencies (2 years)",
    "mo_sin_old_il_acct": "Oldest Installment Account Age",
    "purpose_small_business": "Purpose (Small Business)",
    "num_bc_sats": "Satisfactory Bankcards",
    "percent_bc_gt_75": "Bankcards Above 75% Limit",
    "num_tl_op_past_12m": "Accounts Opened (12 months)",
    "mo_sin_rcnt_tl": "Months Since Last Account",
    "home_ownership_MORTGAGE": "Home Ownership (Mortgage)",
    "num_actv_bc_tl": "Active Bankcards",
}


def get_friendly_label(feature_name):
    """returns a human-friendly label for a feature name"""
    return FRIENDLY_LABELS.get(feature_name, feature_name)