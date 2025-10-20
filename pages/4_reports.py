import streamlit as st
import pandas as pd
from utils.compliance import check_compliance
import io

st.title("Reports")

if "positions_df" not in st.session_state:
    st.warning("Please upload and validate your StockTrak data on the Upload page.")
    st.stop()

positions_df = st.session_state["positions_df"]
portfolio_value = st.session_state["portfolio_value"]
cash = st.session_state["cash"]
trades = st.session_state["trades"]

metrics, status = check_compliance(positions_df, portfolio_value, cash, trades)

# Download compliance summary
summary = {
    "Portfolio Value": [metrics["portfolio_value"]],
    "Cash Balance": [metrics["cash_balance"]],
    "Long Count": [metrics["long_count"]],
    "Short Count": [metrics["short_count"]],
    "Dollar Neutrality": [metrics["dn_ratio"]],
    "Cash %": [metrics["cash_pct"]],
    "Penalty Points": [status["penalty_points"]],
}
df_summary = pd.DataFrame(summary)

st.subheader("Compliance Summary")
st.dataframe(df_summary)

csv = df_summary.to_csv(index=False)
st.download_button(
    "Download Compliance Report CSV",
    csv,
    "compliance_report.csv",
    "text/csv"
)

st.markdown("---")
st.write("Save your weekly results for history and tracking progress!")
