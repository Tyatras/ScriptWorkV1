import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime

# Set page config
st.set_page_config(page_title="Report Polisher", layout="centered")
st.title("🧼 Report Polisher")

# --- Step 1: Inputs ---
st.subheader("📥 Upload and Customize Report")

with st.form("report_form"):
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Company Name", max_chars=100)
    with col2:
        report_type = st.selectbox("Report Type", [
            "Transactions Export",
            "Balance Report",
            "Balance Report Expanded",
            "Custom Report"
        ])

    date_range = st.text_input("Date or Date Range", placeholder="e.g., Jan 2024 or 01/01/24 - 01/31/24")
    uploaded_file = st.file_uploader("Upload CSV Report", type="csv")

    submitted = st.form_submit_button("✅ Generate Polished Report")

# --- Step 2: Process and Output ---
if submitted and uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        # Preview original CSV
        st.subheader("🔍 Original Report Preview")
        st.dataframe(df.head())

        # Create header rows
        header = pd.DataFrame({
            df.columns[0]: [company_name, report_type, date_range]
        })

        # Concatenate headers with data
        full_report = pd.concat([header, df], ignore_index=True)

        # Generate filename
        clean_company = company_name.replace(" ", "").replace(",", "")
        clean_type = report_type.replace(" ", "")
        clean_date = date_range.replace(" ", "").replace("/", "-").replace(",", "")
        output_name = f"{clean_company}_{clean_type}_{clean_date}_polished.csv"

        # Download
        csv_out = full_report.to_csv(index=False)
        st.subheader("📤 Download Your Polished Report")
        st.download_button(
            label=f"📥 Download {output_name}",
            data=csv_out,
            file_name=output_name,
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

elif submitted:
    st.warning("⚠️ Please upload a CSV file to proceed.")
