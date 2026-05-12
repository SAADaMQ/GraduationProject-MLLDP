"""
similar borrowers component
displays the 10 most similar past borrowers from the lookup pool

renders each row as a separate markdown call (same approach as top risk factors)
to avoid streamlit's html parser breaking on large nested html
"""

import streamlit as st


def render_similar_borrowers(knn_result):
    """
    render summary stats and a clean row-based view of similar borrowers
    """
    n_defaulted = knn_result["n_defaulted"]
    n_paid = knn_result["n_paid"]
    total = knn_result["total"]
    similar = knn_result["similar"]

    # summary stats at top
    default_pct = (n_defaulted / total) * 100 if total > 0 else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Similar Borrowers",
            value=total,
            help="Closest matches from past loans",
        )
    with col2:
        st.metric(
            label="Defaulted",
            value=f"{n_defaulted} ({default_pct:.0f}%)",
        )
    with col3:
        st.metric(
            label="Paid in Full",
            value=f"{n_paid} ({100-default_pct:.0f}%)",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # sort: defaulted first then by distance ascending
    sorted_similar = sorted(
        enumerate(similar, start=1),
        key=lambda x: (-x[1]["outcome"], x[1]["distance"]),
    )

    # column headers
    header_html = """
    <div style="
        display: grid;
        grid-template-columns: 60px 1fr 1fr;
        padding: 0.8rem 1rem;
        background: #0A2540;
        color: white;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        font-size: 0.9rem;
    ">
        <div style="text-align: center;">#</div>
        <div>Outcome</div>
        <div style="text-align: right;">Model Risk</div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

  # render each row as its own markdown call
    for original_rank, s in sorted_similar:
        is_default = s["outcome"] == 1
        outcome_label = "DEFAULTED" if is_default else "Paid"
        outcome_icon = "❌" if is_default else "✅"

        if is_default:
            outcome_color = "#FFFFFF" 
            outcome_bg = "#DC2626"       
            risk_color = "#FFFFFF"  
            rank_color = "#FFFFFF"           
            font_weight = "700"
        else:
            outcome_color = "#10B981" 
            outcome_bg = "#FFFFFF"  
            risk_color = "#0A2540"
            rank_color = "#6B7280"
            font_weight = "600"

        proba_pct = s["probability"] * 100

        row_html = f"""
        <div style="
            display: grid;
            grid-template-columns: 60px 1fr 1fr;
            padding: 0.9rem 1rem;
            background: {outcome_bg};
            border-bottom: 1px solid #E5E7EB;
            align-items: center;
        ">
            <div style="text-align: center; color: {rank_color}; font-weight: 600;">
                {original_rank}
            </div>
            <div style="color: {outcome_color}; font-weight: {font_weight};">
                {outcome_icon} {outcome_label}
            </div>
            <div style="
                text-align: right;
                font-family: 'Roboto Mono', monospace;
                color: {risk_color};
                font-weight: 600;
            ">
                {proba_pct:.1f}%
            </div>
        </div>
        """
        st.markdown(row_html, unsafe_allow_html=True)

    st.caption(
        f"Of the {total} most similar past borrowers, "
        f"{n_defaulted} defaulted (shown in red) and {n_paid} paid in full."
    )