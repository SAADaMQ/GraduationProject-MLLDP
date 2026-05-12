"""
score bar component
horizontal bar from 0 to 100 with 3 zones, tick marks, dividers,
and an arrow pointing to the current score position

includes a fill-in animation on first render
"""

import streamlit as st
from config.constants import ZONE_APPROVE_MAX, ZONE_HIGH_RISK_MAX


def render_score_bar(score):
    """
    render the 3-zone score bar with arrow indicator
    score is 0-100
    """
    score_clamped = max(0, min(100, score))

    # 3-color gradient with hard color stops at the zone boundaries
    gradient = (
        f"linear-gradient(to right, "
        f"#10B981 0%, #10B981 {ZONE_APPROVE_MAX}%, "
        f"#F59E0B {ZONE_APPROVE_MAX}%, #F59E0B {ZONE_HIGH_RISK_MAX}%, "
        f"#DC2626 {ZONE_HIGH_RISK_MAX}%, #DC2626 100%)"
    )

    bar_html = f"""
    <style>
        @keyframes growIn {{
            0% {{ width: 0%; }}
            100% {{ width: {score_clamped}%; }}
        }}
        @keyframes dropDown {{
            0% {{ transform: translateY(-15px); opacity: 0; }}
            100% {{ transform: translateY(0); opacity: 1; }}
        }}
        .score-display {{
            font-family: 'Roboto Mono', monospace;
            font-size: 4rem;
            font-weight: 700;
            color: #0A2540;
            text-align: center;
            margin-bottom: 0.3rem;
            line-height: 1;
        }}
        .score-label {{
            text-align: center;
            color: #6B7280;
            font-size: 1rem;
            margin-bottom: 2rem;
        }}
        .bar-wrapper {{
            position: relative;
            padding-top: 30px;
            margin-bottom: 3rem;
        }}
        .score-arrow {{
            position: absolute;
            top: 0;
            left: {score_clamped}%;
            transform: translateX(-50%);
            animation: dropDown 0.6s ease-out 1.2s both;
            text-align: center;
            font-family: 'Roboto Mono', monospace;
        }}
        .arrow-value {{
            background: #0A2540;
            color: white;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 700;
            display: inline-block;
            white-space: nowrap;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }}
        .arrow-tip {{
            width: 0;
            height: 0;
            border-left: 7px solid transparent;
            border-right: 7px solid transparent;
            border-top: 9px solid #0A2540;
            margin: 0 auto;
            margin-top: -1px;
        }}
        .bar-container {{
            position: relative;
            width: 100%;
            height: 36px;
            background: {gradient};
            border-radius: 18px;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);
            overflow: hidden;
        }}
        .bar-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: {score_clamped}%;
            background: rgba(255,255,255,0.18);
            border-right: 3px solid white;
            animation: growIn 1.2s ease-out;
        }}
        .zone-divider {{
            position: absolute;
            top: -8px;
            height: 52px;
            width: 2px;
            background: rgba(255,255,255,0.8);
            box-shadow: 0 0 4px rgba(0,0,0,0.3);
        }}
        .zone-divider-17 {{
            left: {ZONE_APPROVE_MAX}%;
        }}
        .zone-divider-50 {{
            left: {ZONE_HIGH_RISK_MAX}%;
        }}
        .tick-marks {{
            position: relative;
            margin-top: 0.4rem;
            height: 24px;
        }}
        .tick {{
            position: absolute;
            transform: translateX(-50%);
            font-size: 0.75rem;
            color: #6B7280;
            font-family: 'Roboto Mono', monospace;
        }}
        .tick.major {{
            color: #0A2540;
            font-weight: 600;
            font-size: 0.85rem;
        }}
        .tick.threshold-tick {{
            color: #F59E0B;
            font-size: 0.8rem;
        }}
        .tick.boundary-tick {{
            color: #DC2626;
            font-size: 0.8rem;
        }}
        .zone-labels {{
            display: flex;
            margin-top: 1rem;
            font-size: 0.95rem;
            font-weight: 600;
            text-align: center;
        }}
        .zone-segment {{
            padding: 0.4rem 0;
            border-radius: 6px;
            margin: 0 2px;
        }}
        .zone-approve {{
            color: white;
            background: #10B981;
            width: {ZONE_APPROVE_MAX}%;
        }}
        .zone-risk {{
            color: white;
            background: #F59E0B;
            width: {ZONE_HIGH_RISK_MAX - ZONE_APPROVE_MAX}%;
        }}
        .zone-reject {{
            color: white;
            background: #DC2626;
            width: {100 - ZONE_HIGH_RISK_MAX}%;
        }}
    </style>

    <div class="score-display">{score_clamped:.1f} / 100</div>
    <div class="score-label">Risk Score (lower is better)</div>

    <div class="bar-wrapper">
        <div class="score-arrow">
            <div class="arrow-value">{score_clamped:.1f}</div>
            <div class="arrow-tip"></div>
        </div>
        <div class="bar-container">
            <div class="bar-overlay"></div>
            <div class="zone-divider zone-divider-17"></div>
            <div class="zone-divider zone-divider-50"></div>
        </div>
        <div class="tick-marks">
            <div class="tick major" style="left: 0%;">0</div>
            <div class="tick" style="left: 10%;">10</div>
            <div class="tick threshold-tick" style="left: 17%;">
                <div style="font-weight: 700;">17</div>
                <div style="font-size: 0.65rem; margin-top: 2px;">threshold</div>
            </div>
            <div class="tick" style="left: 25%;">25</div>
            <div class="tick" style="left: 35%;">35</div>
            <div class="tick boundary-tick" style="left: 50%;">
                <div style="font-weight: 700;">50</div>
                <div style="font-size: 0.65rem; margin-top: 2px;">high-risk cap</div>
            </div>
            <div class="tick" style="left: 65%;">65</div>
            <div class="tick" style="left: 80%;">80</div>
            <div class="tick major" style="left: 100%;">100</div>
        </div>
    </div>

    <div class="zone-labels">
        <div class="zone-segment zone-approve">🟢 APPROVE (0&ndash;17)</div>
        <div class="zone-segment zone-risk">🟠 HIGH RISK (17&ndash;50)</div>
        <div class="zone-segment zone-reject">🔴 REJECT (50&ndash;100)</div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)