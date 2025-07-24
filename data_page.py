#data_page.py

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
import pandas as pd
import re
from io import BytesIO

def extract_data_from_invoice(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    text = " ".join([page.page_content for page in pages])

    data = {
        "Invoice Number": re.search(r"Invoice Number[:\s]*([^\n]+)", text),
        "Invoice Date": re.search(r"Invoice Date[:\s]*([^\n]+)", text),
        "Order Number": re.search(r"Order Number[:\s]*([^\n]+)", text),
        "Order Date": re.search(r"Order Date[:\s]*([^\n]+)", text),
        "Billing Address": re.search(r"Billing Address[:\s]*(.+?)(?=\n|Shipping|Invoice)", text, re.DOTALL),
        "Shipping Address": re.search(r"Shipping Address[:\s]*(.+?)(?=\n|Invoice|Total)", text, re.DOTALL),
        "Tax / GST": re.search(r"Tax(?: Rate)?[:\s]*([^\n]+)", text),
        "Total Amount": re.search(r"Total Amount[:\s]*([^\n]+)", text),
    }

    structured_data = {key: match.group(1).strip() if match else "Not found" for key, match in data.items()}
    return structured_data

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Invoice Data')
    return output.getvalue()

def show_data_page():
    st.set_page_config(page_title="Structured Invoice Data")
    st.title("📊 Structured Invoice Data")

    try:
        data = extract_data_from_invoice("invoice.pdf")

        # Display structured data
        st.subheader("📌 Key Invoice Fields")
        df = pd.DataFrame(list(data.items()), columns=["Field", "Value"])
        st.table(df)

        # Download as Excel
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="📥 Download as Excel",
            data=excel_data,
            file_name="invoice_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.warning("⚠️ Please upload a valid invoice on the chatbot page first.")
        st.error(str(e))


