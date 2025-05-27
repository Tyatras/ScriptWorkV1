import streamlit as st
import pandas as pd

st.set_page_config(page_title="FMV Adjustment Calculator", layout="centered")
st.title("📊 FMV Adjustment Calculator")
st.write("Upload two CSV files to calculate FMV adjustments based on asset data.")

# Upload files
sheet1_file = st.file_uploader("Upload Reference Data (sheet1.csv)", type="csv", key="sheet1")
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

        # Merge Confirm FMV from Sheet 1 into Sheet 2
        merged = df2.merge(df1[['asset', 'confirm fmv']], how='left', on='asset')
        merged.rename(columns={'confirm fmv': 'fmv'}, inplace=True)

        # Calculate FMV Adjustment
        def calculate_adjustment(row):
            try:
                if pd.isna(row['qty']) or row['qty'] == 0:
                    return 0.0
                return row['qty'] * row['fmv']
            except:
                return 0.0

        merged['fmv adjustment'] = merged.apply(calculate_adjustment, axis=1)

        # Show results
        st.subheader("Updated Transactions Table")
        st.dataframe(merged)

        # Allow download
        csv = merged.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Updated Sheet",
            data=csv,
            file_name="updated_transactions.csv",
            mime="text/csv"
        )
else:
    st.info("Please upload both CSV files to begin.")

