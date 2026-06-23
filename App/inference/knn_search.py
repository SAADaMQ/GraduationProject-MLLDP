"""
k-nearest neighbours search on the lookup pool
finds the 10 most similar past applicants for case-based context
"""

import numpy as np
from config.constants import NUM_SIMILAR_BORROWERS


def find_similar_borrowers(preprocessed_df, bundle):
    """
    finds the N most similar borrowers from the lookup pool
    using euclidean distance on the 40 scaled features

    returns a dict with their indices distances outcomes probabilities
    """
    pool = bundle["lookup_pool"]
    pool_features = pool["features"]
    pool_outcomes = pool["outcomes"]
    pool_probabilities = pool["probabilities"]

    # convert applicant input to a numpy array
    applicant = preprocessed_df.iloc[0].values

    # euclidean distance from applicant to every pool row
    diffs = pool_features - applicant
    distances = np.sqrt((diffs ** 2).sum(axis=1))

    # get indices of the N smallest distances
    nearest_idx = np.argsort(distances)[:NUM_SIMILAR_BORROWERS]

    similar = []
    for i in nearest_idx:
        similar.append({
            "distance": float(distances[i]),
            "outcome": int(pool_outcomes[i]),
            "probability": float(pool_probabilities[i]),
        })

    # count how many defaulted vs paid among the similar group
    n_defaulted = sum(1 for s in similar if s["outcome"] == 1)
    n_paid = len(similar) - n_defaulted

    return {
        "similar": similar,
        "n_defaulted": n_defaulted,
        "n_paid": n_paid,
        "total": len(similar),
    }