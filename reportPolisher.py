import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime

st.set_page_config(page_title="Report Polisher", layout="centered")
st.title("🧼 Report Polisher")

st.markdown("""
This app lets you upload a CSV, apply a professional header with your custom inputs, and download a polished report.
""")

# Input form
with st.form("user_input_form"):
    company_name = st.text_input("🏢 Company Name")

    report_options = [
        "Transaction Export", "Balance Report", "Balance Check Report",
        "Balance Report Expanded", "Journal Entry Report Expanded",
        "General Ledger Summary Report", "General Ledger Detail Report",
        "Valuation Rollforward Report", "Cost Basis Roll Forward",
        "Actions Report", "Ledger Report", "Dashboard Summary Report",
        "Dashboard Results Report", "Custom Report"
    ]

    report_type = st.selectbox("📋 Report Type", options=report_options)
    date_range = st.text_input("📅 Date or Date Range (e.g. Jan 2024, 01/01/2024 - 01/31/2024)")

    uploaded_file = st.file_uploader("📥 Upload CSV Report", type="csv")

    submitted = st.form_submit_button("✨ Polish Report")

if submitted and uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        preview_df = df.copy()

        # Create header rows
        header_rows = pd.DataFrame({
            df.columns[0]: [company_name, report_type, date_range]
        })

        # Concatenate header with original content
        polished_report = pd.concat([header_rows, df], ignore_index=True)

        # Generate polished filename
        clean_company = company_name.replace(" ", "").replace("/", "-")
        clean_report = report_type.replace(" ", "").replace("/", "-")
        clean_date = date_range.replace(" ", "").replace("/", "-")

        polished_filename = f"{clean_company}_{clean_report}_{clean_date}_polished.csv"

        st.subheader("📄 Preview")
        st.dataframe(preview_df.head())

        # Downloadable output
        csv_output = polished_report.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📤 Download Polished Report",
            data=csv_output,
            file_name=polished_filename,
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")

elif submitted and not uploaded_file:
    st.warning("⚠️ Please upload a CSV file to continue.")

elif submitted:
    st.warning("⚠️ Please upload a CSV file to proceed.")
