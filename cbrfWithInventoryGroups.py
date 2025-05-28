import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Cost Basis Roll Forward Calculator", layout="centered")
st.title("📊 Cost Basis Roll Forward Calculator")

# Downloadable CSV template
template = pd.DataFrame(columns=[
    "Asset", "action", "assetUnitAdj", "costBasisAcquired",
    "fairMarketValueDisposed", "shortTermGainLoss", "longTermGainLoss", "isInternalTransfer"
])

csv_template = StringIO()
template.to_csv(csv_template, index=False)

st.download_button(
    label="📄 Download Example CSV Template",
    data=csv_template.getvalue(),
    file_name="example_action_data_template.csv",
    mime="text/csv"
)

# File upload
uploaded_file = st.file_uploader("Upload Action-Level CSV File", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()

    required_cols = [
        "asset", "action", "assetunitadj", "costbasisacquired",
        "fairmarketvaluedisposed", "shorttermgainloss", "longtermgainloss", "isinternaltransfer"
    ]

    if not all(col in df.columns for col in required_cols):
        st.error("❌ CSV file is missing one or more required columns.")
    else:
        if st.button("✅ Calculate Cost Basis Roll Forward"):
            # Filter out internal transfers (0 or blank)
            filtered = df[(df['isinternaltransfer'].fillna(1) != 0)]

            # Group by asset and aggregate
            grouped = filtered.groupby("asset").agg({
                "assetunitadj": [
                    lambda x: x[df.loc[x.index, 'action'] == 'buy'].sum(),  # Qty (acq)
                    lambda x: x[df.loc[x.index, 'action'] == 'sell'].sum()  # Qty (disp)
                ],
                "costbasisacquired": lambda x: x[df.loc[x.index, 'action'] == 'buy'].sum(),
                "fairmarketvaluedisposed": lambda x: x[df.loc[x.index, 'action'] == 'sell'].sum(),
                "shorttermgainloss": "sum",
                "longtermgainloss": "sum"
            }).reset_index()

            grouped.columns = [
                "Asset", "Qty (acq)", "Qty (disp)", "Cost Basis (acq)",
                "Proceeds From Disposal", "ST Gain Loss", "LT Gain Loss"
            ]

            st.subheader("📘 Cost Basis Summary Table")
            st.dataframe(grouped)

            csv = grouped.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Summary CSV",
                data=csv,
                file_name="cost_basis_summary.csv",
                mime="text/csv"
            )
else:
    st.info("Please upload a CSV file to continue.")
