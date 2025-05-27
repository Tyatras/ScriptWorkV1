import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="FMV Adjustment Calculator", layout="centered")
st.title("FMV Adjustment Calculator")
st.write("Upload two CSV files to calculate FMV adjustments based on asset data.")

# CSV Template Header
csv_template = StringIO()
pd.DataFrame(columns=[
    "Asset", "Qty", "Cost Basis (Acq)", "Cost Basis (Disp)", "Cost Basis",
    "Fair Market Value", "Unrealized Gain/Loss", "Inventory", "Confirm FMV"
]).to_csv(csv_template, index=False)

# Downloadable CSV template
st.download_button(
    label="📄 Download Inventory Template CSV",
    data=csv_template.getvalue(),
    file_name="InventoryViewsSummaryTemplate.csv",
    mime="text/csv"
)

# Upload files
sheet1_file = st.file_uploader("Upload Reference Data (InventoryViewsSummaryTemplate.csv)", type="csv", key="sheet1")
sheet2_file = st.file_uploader("Upload Transaction Data (sheet2.csv)", type="csv", key="sheet2")

# Add a button to trigger calculation
if sheet1_file and sheet2_file:
    if st.button("✅ Calculate FMV Adjustments"):
        # Load CSVs into DataFrames
        df1 = pd.read_csv(sheet1_file)
        df2 = pd.read_csv(sheet2_file)

        # Normalize column names
        df1.columns = df1.columns.str.strip().str.lower()
        df2.columns = df2.columns.str.strip().str.lower()

        # Deduplicate asset entries to avoid merge duplications
        df1 = df1.drop_duplicates(subset='asset')

        # Merge Confirm FMV from Sheet 1 into Sheet 2
        df2 = df2.merge(df1[['asset', 'confirm fmv']], how='left', on='asset')
        df2.rename(columns={'confirm fmv': 'fmvrate'}, inplace=True)

        # Create new FMV column in Sheet 2
        df2['newfmv'] = df2['qty'].fillna(0) * df2['fmvrate'].fillna(0)

        # Create fmv adj down and up based on carryingvalue - newfmv
        df2['fmv adj down'] = df2.apply(
            lambda row: row['carryingvalue'] - row['newfmv'] if (row['carryingvalue'] - row['newfmv']) < 0 else 0,
            axis=1
        )
        df2['fmv adj up'] = df2.apply(
            lambda row: row['carryingvalue'] - row['newfmv'] if (row['carryingvalue'] - row['newfmv']) > 0 else 0,
            axis=1
        )

        # Show results
        st.subheader("Updated Transactions Table")
        st.dataframe(df2)

        # Allow download
        csv = df2.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Updated Sheet",
            data=csv,
            file_name="updated_transactions.csv",
            mime="text/csv"
        )
else:
    st.info("Please upload both CSV files to begin.")

