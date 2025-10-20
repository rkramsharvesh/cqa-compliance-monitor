import streamlit as st
from utils.compliance import check_compliance
from utils.corrections import generate_corrections

st.title("Correction")

if "positions_df" not in st.session_state:
    st.warning("Please upload and validate your StockTrak data on the Upload page.")
    st.stop()

positions_df = st.session_state["positions_df"]
portfolio_value = st.session_state["portfolio_value"]
cash = st.session_state["cash"]
trades = st.session_state["trades"]

metrics, status = check_compliance(positions_df, portfolio_value, cash, trades)
corrections = generate_corrections(metrics, status, positions_df)

if corrections:
    st.header("Recommended Corrections")
    for i, c in enumerate(corrections, 1):
        st.subheader(f"{i}. {c['category']} — {c['severity']}")
        st.write(f"**Action:** {c['recommendation']}")
        if c.get("amount"):
            st.write(f"**Amount/Threshold:** {c['amount']}")
        if c.get("details"):
            st.write(f"{c['details']}")
else:
    st.success("No corrections needed. Your portfolio is fully compliant!")

st.markdown("---")
st.write("Return to the Dashboard page to see your overall compliance points.")
