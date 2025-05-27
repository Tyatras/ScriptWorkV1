import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="FMV Adjustment Calculator", layout="centered")
st.title("FMV Adjustment Calculator")
st.markdown("""
### 📋 Instructions
1. **Download** the Inventory Views Summary Template CSV using the button below.
2. **Go to** the Inventory View you are using, select the date you wish the FMV Calculation to occur, and click Submit.
3. **Paste** the header from the Inventory Views Summary Template CSV onto your Bitwave-downloaded Summary report.
4. **Confirm** the FMV rate for each asset in the \"Confirm FMV\" column.
5. **Save** your file for easy reference and upload below.
6. **Download** the Lots report for the same date.
7. **Upload** the Lots report below.
""")

# CSV Template Header
csv_template = StringIO()
pd.DataFrame(columns=[
    "Asset", "Qty", "Cost Basis (Acq)", "Cost Basis (Disp)", "Cost Basis",
    "Fair Market Value", "Unrealized Gain/Loss", "Inventory", "Confirm FMV"
]).to_csv(csv_template, index=False)

# Downloadable CSV template
st.download_button(
    label="📄 Inventory Views Summary Template CSV",
    data=csv_template.getvalue(),
    file_name="InventoryViewsSummaryTemplate.csv",
    mime="text/csv"
)

# Upload files
sheet1_file = st.file_uploader("Upload Reference Data (InventoryViewsSummaryTemplate.csv)", type="csv", key="sheet1")
sheet2_file = st.file_uploader("Upload Lots Report (lots_report.csv)", type="csv", key="sheet2")

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

        # Ensure 'costbasis' and 'newfmv' are numeric
        df2['costbasis'] = pd.to_numeric(df2['costbasis'], errors='coerce').fillna(0)
        df2['newfmv'] = pd.to_numeric(df2['newfmv'], errors='coerce').fillna(0)

        # Create fmv adj down and up
        df2['fmv adj down'] = df2.apply(
            lambda row: row['costbasis'] - row['newfmv'] if row['costbasis'] > row['newfmv'] else 0,
            axis=1
        )
        df2['fmv adj up'] = df2.apply(
            lambda row: row['newfmv'] - row['costbasis'] if row['costbasis'] < row['newfmv'] else 0,
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
