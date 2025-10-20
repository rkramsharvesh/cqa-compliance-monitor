# utils/compliance.py
import pandas as pd

def check_compliance(positions_df, portfolio_value, cash, trades):
    """
    Check core compliance metrics from given positions dataframe and summary inputs.
    Returns compliance results dict.
    """
    long_positions = positions_df[positions_df['Quantity'] > 0]
    short_positions = positions_df[positions_df['Quantity'] < 0]

    long_count = len(long_positions)
    short_count = len(short_positions)
    long_mv = long_positions['MarketValue'].sum()
    short_mv = short_positions['MarketValue'].sum()

    cash_pct = (cash / portfolio_value * 100) if portfolio_value > 0 else 0
    dn_ratio = (long_mv / short_mv) if short_mv > 0 else 0

    positions_df['PositionWeight'] = (abs(positions_df['MarketValue']) / portfolio_value * 100)

    # Pack up basic metrics
    metrics = {
        'portfolio_value': portfolio_value,
        'cash_balance': cash,
        'cash_pct': cash_pct,
        'long_mv': long_mv,
        'short_mv': short_mv,
        'dn_ratio': dn_ratio,
        'long_count': long_count,
        'short_count': short_count,
        'total_trades': trades,
        'trades_remaining': 1000 - trades
    }

    # Pack up status
    status = {}

    status["long"] = ("Compliant" if long_count >= 40 else "Minor" if long_count >= 38 else "Major")
    status["short"] = ("Compliant" if short_count >= 40 else "Minor" if short_count >= 38 else "Major")
    status["dn"] = ("Compliant" if 0.9 <= dn_ratio <= 1.1 else "Minor" if (0.85 <= dn_ratio < 0.9) or (1.1 < dn_ratio <= 1.18) else "Major")
    status["cash"] = ("Compliant" if cash_pct <= 5 else "Minor" if 6 <= cash_pct <= 8 else "Major")
    status["trades"] = ("Compliant" if trades <= 1000 else "Major")

    # Collect position weight violations
    major_wt = positions_df[positions_df['PositionWeight'] >= 9]
    minor_wt = positions_df[(positions_df['PositionWeight'] >= 6) & (positions_df['PositionWeight'] < 9)]

    status["major_weights"] = major_wt[["Symbol", "PositionWeight"]].to_dict(orient="records")
    status["minor_weights"] = minor_wt[["Symbol", "PositionWeight"]].to_dict(orient="records")

    # Penalty calculation
    penalty_pts = (
         (1 if status["long"] == "Minor" else 0) + (3 if status["long"] == "Major" else 0)
        + (1 if status["short"] == "Minor" else 0) + (3 if status["short"] == "Major" else 0)
        + (1 if status["dn"] == "Minor" else 0) + (3 if status["dn"] == "Major" else 0)
        + (1 if status["cash"] == "Minor" else 0) + (3 if status["cash"] == "Major" else 0)
        + (3 if status["trades"]=="Major" else 0)
        + len(major_wt)*3 + len(minor_wt)*1
    )

    status["penalty_points"] = min(penalty_pts, 5)  # max 5 per week

    return metrics, status
