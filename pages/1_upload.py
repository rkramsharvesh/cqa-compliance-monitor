import streamlit as st
import pandas as pd

st.title("Upload")

st.write("""
Upload your StockTrak open positions file (CSV or XLSX).
""")

uploaded_file = st.file_uploader("Open Positions Export", type=["csv", "xlsx"])

portfolio_value = st.number_input("Current Portfolio Value ($)", min_value=0.0, value=1000000.0, step=1000.0)
cash_balance = st.number_input("Cash Balance ($)", min_value=0.0, value=50000.0, step=1000.0)
trade_count = st.number_input("Total Trades Made", min_value=0, value=0, step=1)

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully.")
        st.write(df.head())

        # Save to session state for other pages to use
        st.session_state["positions_df"] = df
        st.session_state["portfolio_value"] = portfolio_value
        st.session_state["cash"] = cash_balance
        st.session_state["trades"] = trade_count

    except Exception as e:
        st.error(f"Failed to parse file: {str(e)}")
else:
    st.info("Waiting for a StockTrak file upload...")

st.markdown("---")
st.write("Proceed to the **Dashboard** page after uploading your data.")
