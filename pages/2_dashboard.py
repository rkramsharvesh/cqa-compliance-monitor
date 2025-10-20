import streamlit as st
from utils.compliance import check_compliance

st.title("Compliance Dashboard")

# Check for uploaded data in session state
if "positions_df" not in st.session_state:
    st.warning("Please upload your StockTrak data on the Upload page first.")
    st.stop()

positions_df = st.session_state["positions_df"]
portfolio_value = st.session_state["portfolio_value"]
cash = st.session_state["cash"]
trades = st.session_state["trades"]

metrics, status = check_compliance(positions_df, portfolio_value, cash, trades)

st.header("Key Compliance Metrics")
st.write(f"Portfolio Value: **${portfolio_value:,.0f}**")
st.write(f"Cash Balance: **${cash:,.0f}** ({metrics['cash_pct']:.2f}%)")
st.write(f"Long Stocks: **{metrics['long_count']}**, Short Stocks: **{metrics['short_count']}**")
st.write(f"Dollar Neutrality Ratio: **{metrics['dn_ratio']:.3f}** (Target: 0.9-1.1)")
st.write(f"Trade Count: **{metrics['total_trades']}** (Remaining: {metrics['trades_remaining']})")

st.header("Compliance Status")
compliance_keys = ["long", "short", "dn", "cash", "trades"]
names = {
    "long": "Long Stock Count",
    "short": "Short Stock Count",
    "dn": "Dollar Neutrality",
    "cash": "Cash Holdings",
    "trades": "Trade Limit",
}

for key in compliance_keys:
    st.write(f"{names[key]}: **{status[key]} violation**" if status[key] != "Compliant" else f"{names[key]}: Compliant")

if status.get("major_weights", []):
    st.subheader("Major Position Weight Violations")
    for entry in status["major_weights"]:
        st.error(f"{entry['Symbol']}: {entry['PositionWeight']:.2f}% (Major)")

if status.get("minor_weights", []):
    st.subheader("Minor Position Weight Violations")
    for entry in status["minor_weights"]:
        st.warning(f"{entry['Symbol']}: {entry['PositionWeight']:.2f}% (Minor)")

st.markdown("---")
st.write(f"**Weekly Penalty Points:** {status['penalty_points']} (max 5)")
