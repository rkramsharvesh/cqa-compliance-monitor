"""
corrections.py
--------------
This module contains functions to numerically recommend compliance corrections
based on detected violations for the CQA Investment Challenge.
It does NOT recommend individual stocks—only the quantities/dollars to adjust.

Functions:
    - generate_corrections: Given compliance metrics and violations,
      outputs precise actions to correct each type of violation, including
      share counts, dollar values, and estimated trade impact.
"""

def generate_corrections(metrics, status, positions_df):
    corrections = []

    # Long stock count
    if status['long'] in ['Minor', 'Major'] and metrics['long_count'] < 40:
        shortage = 40 - metrics['long_count']
        avg_size = metrics['long_mv'] / max(metrics['long_count'], 1)
        corrections.append({
            "category": "Long Stock Count",
            "severity": status['long'],
            "recommendation": f"Add {shortage} new long position(s)",
            "amount": f"~${avg_size:,.0f} each",
            "details": f"Allocate at least ${avg_size*shortage:,.0f} across {shortage} new long positions."
        })
    # Short stock count
    if status['short'] in ['Minor', 'Major'] and metrics['short_count'] < 40:
        shortage = 40 - metrics['short_count']
        avg_size = metrics['short_mv'] / max(metrics['short_count'], 1)
        corrections.append({
            "category": "Short Stock Count",
            "severity": status['short'],
            "recommendation": f"Add {shortage} new short position(s)",
            "amount": f"~${avg_size:,.0f} each",
            "details": f"Allocate at least ${avg_size*shortage:,.0f} across {shortage} new shorts."
        })
    # Dollar neutrality
    if status['dn'] in ['Minor', 'Major']:
        dn_ratio = metrics['dn_ratio']
        L, S = metrics['long_mv'], metrics['short_mv']
        if dn_ratio > 1.1:
            excess = L - S*1.0
            corrections.append({
                "category": "Dollar Neutrality",
                "severity": status['dn'],
                "recommendation": "Reduce long exposures or add to shorts",
                "amount": f"Reduce longs by ${excess:,.0f} OR add same value to short side.",
                "details": f"(Current DN: {dn_ratio:.3f})."
            })
        elif dn_ratio < 0.9:
            excess = S - L*1.0
            corrections.append({
                "category": "Dollar Neutrality",
                "severity": status['dn'],
                "recommendation": "Reduce short exposures or add to longs",
                "amount": f"Reduce shorts by ${excess:,.0f} OR add same value to long side.",
                "details": f"(Current DN: {dn_ratio:.3f})."
            })
    # Cash holdings
    if status['cash'] in ['Minor', 'Major']:
        excess_cash = metrics['cash_balance'] - metrics['portfolio_value']*0.05
        if excess_cash > 0:
            corrections.append({
                "category": "Cash Held",
                "severity": status['cash'],
                "recommendation": f"Invest ${excess_cash:,.0f} to reduce cash to ≤5%",
                "amount": "",
                "details": "Split between long and short as needed to maintain dollar neutrality."
            })
    # Position weights
    # Major violations
    for wt in status.get("major_weights", []):
        symbol = wt["Symbol"]
        weight = wt["PositionWeight"]
        corrections.append({
            "category": "Position Weight",
            "severity": "Major",
            "recommendation": f"Reduce {symbol} to <5%",
            "amount": f"Current weight: {weight:.2f}%",
            "details": "Sell enough shares to bring this below 5%."
        })
    # Minor violations
    for wt in status.get("minor_weights", []):
        symbol = wt["Symbol"]
        weight = wt["PositionWeight"]
        corrections.append({
            "category": "Position Weight",
            "severity": "Minor",
            "recommendation": f"Trim {symbol} closer to 5%",
            "amount": f"Current weight: {weight:.2f}%",
            "details": "Sell or cover to reduce position."
        })

    return corrections
