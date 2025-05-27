import streamlit as st
import pandas as pd

st.set_page_config(page_title="FMV Adjustment Calculator", layout="centered")
st.title("📊 FMV Adjustment Calculator")
st.write("Upload two CSV files to calculate FMV adjustments based on asset data.")

# Upload files
sheet1_file = st.file_uploader("Upload Reference Data (sheet1.csv)", type="csv", key="sheet1")
sheet2_file = st.file_uploader("Upload Transaction Data (sheet2.csv)", type="csv", key="sheet2")

if sheet1_file and sheet2_file:
    # Load CSVs into DataFrames
    df1 = pd.read_csv(sheet1_file)
    df2 = pd.read_csv(sheet2_file)

    # Normalize column names
    df1.columns = df1.columns.str.strip().str.lower()
    df2.columns = df2.columns.str.strip().str.lower()

    # Merge Confirm FMV from Sheet 1 into Sheet 2

