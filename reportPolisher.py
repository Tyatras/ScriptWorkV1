import streamlit as st
import pandas as pd
from io import StringIO
import datetime

st.set_page_config(page_title="📁 Report Polisher", layout="centered")
st.title("📁 Report Polisher")

st.markdown("""
This tool allows you to upload a CSV report and generate a polished version with a professional header.
""")

with st.form("input_form"):
    company_name = st.text_input("Company Name")
    report_type = st.selectbox(
        "Report Type",
        [
            "Transaction Export",
            "Balance Report",
            "Balance Check Report",
            "Balance Report Expanded",
            "Journal Entry Report Expanded",
            "General Ledger Summary Report",
            "General Ledger Detail Report",
            "Valuation Rollforward Report",
            "Cost Basis Roll Forward",
            "Actions Report",
            "Ledger Report",
            "Dashboard Summary Report",
            "Dashboard Results Report",
            "Custom Report"
        ]
    )
    custom_report_type = ""
    if report_type == "Custom Report":
        custom_report_type = st.text_input("Enter Custom Report Type")
    date_range = st.text_input("Date or Date Range", placeholder="e.g., Jan 2024")
    uploaded_file = st.file_uploader("Upload CSV Report", type="csv")
    submit_button = st.form_submit_button("Polish Report")

if submit_button and uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        final_report_type = custom_report_type if report_type == "Custom Report" and custom_report_type else report_type

        # Create header row aligned with columns A, B, and C
        header_data = ["" for _ in df.columns]
        if len(header_data) >= 3:
            header_data[0] = company_name
            header_data[1] = final_report_type
            header_data[2] = date_range
        else:
            for i, val in enumerate([company_name, final_report_type, date_range]):
                if i < len(header_data):
                    header_data[i] = val

        header_row = pd.DataFrame([header_data], columns=df.columns)
        blank_row = pd.DataFrame([["" for _ in df.columns]], columns=df.columns)

        # Combine header, blank line, and original report
        polished_df = pd.concat([header_row, blank_row, df], ignore_index=True)

        st.subheader("📋 Polished Report Preview")
        st.dataframe(polished_df, use_container_width=True)

        filename = f"{company_name.replace(' ', '')}_{final_report_type.replace(' ', '')}_{date_range.replace(' ', '')}.csv"
        csv = polished_df.to_csv(index=False, header=False)

        st.download_button(
            label="📅 Download Polished CSV",
            data=csv,
            file_name=filename,
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please fill out all fields and upload a CSV file to polish your report.")
