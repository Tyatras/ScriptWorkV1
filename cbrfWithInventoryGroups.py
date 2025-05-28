import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Cost Basis Roll Forward Calculator", layout="centered")
st.title("\U0001F4CA Cost Basis Roll Forward Calculator")

# Downloadable CSV template
template = pd.DataFrame(columns=[
    "Asset", "action", "assetUnitAdj", "costBasisAcquired",
    "fairMarketValueDisposed", "shortTermGainLoss", "longTermGainLoss", "isInternalTransfer"
])

csv_template = StringIO()
template.to_csv(csv_template, index=False)

st.download_button(
    label="\U0001F4C4 Download Example CSV Template",
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
            filtered = df[(df['isinternaltransfer'].isna()) | (df['isinternaltransfer'] == 0)]

            # Calculate pivot values
            summary = filtered.groupby('asset').apply(lambda x: pd.Series({
                "Qty (acq)": x[(x['action'] == 'buy')]['assetunitadj'].sum(),
                "Cost Basis (acq)": x[(x['action'] == 'buy')]['costbasisacquired'].sum(),
                "Qty (disp)": x[(x['action'] == 'sell')]['assetunitadj'].sum(),
                "Proceeds From Disposal": x[(x['action'] == 'sell')]['fairmarketvaluedisposed'].sum(),
                "ST Gain Loss": x['shorttermgainloss'].sum(),
                "LT Gain Loss": x['longtermgainloss'].sum()
            })).reset_index()

            st.subheader("\U0001F4D8 Cost Basis Summary Table")
            st.dataframe(summary)

            csv = summary.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="\U0001F4E5 Download Summary CSV",
                data=csv,
                file_name="cost_basis_summary.csv",
                mime="text/csv"
            )
else:
    st.info("Please upload a CSV file to continue.")
