"""
google_sheet.py
-----------------------------------
Loads data from Google Sheets.
Compatible with both Local PC and
Streamlit Cloud deployment.
"""

import pandas as pd
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

# ==========================================
# GOOGLE API SCOPES
# ==========================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


# ==========================================
# GOOGLE CLIENT
# ==========================================

def get_client():
    """
    Creates Google Sheets client.
    """

    # -------- Streamlit Cloud --------
    if "gcp_service_account" in st.secrets:

        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )

    # -------- Local Computer --------
    else:

        creds = Credentials.from_service_account_file(
            "service_account.json",
            scopes=SCOPES
        )

    return gspread.authorize(creds)


# ==========================================
# LOAD DATA
# ==========================================


def load_jainam_data():
    """
    Loads Jainam worksheet every 30 seconds.
    """

    client = get_client()
    workbook = client.open("test_streamlit")
    worksheet = workbook.worksheet("Jainam")
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)

    # ==========================================
    # Clean Column Names
    # ==========================================

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
    )

    # ==========================================
    # Remove TOTAL row
    # ==========================================

    if "UserID" in df.columns:

        df = df[
            df["UserID"]
            .astype(str)
            .str.upper()
            != "TOTAL"
        ]

    # ==========================================
    # Required Columns
    # ==========================================

    required_columns = [
        "UserID",
        "ALLOCATION",
        "Main_Allocation"
    ]

    for col in required_columns:

        if col not in df.columns:
            raise Exception(f"Column '{col}' not found in Google Sheet.")

    # ==========================================
    # Convert Numbers
    # ==========================================

    df["ALLOCATION"] = pd.to_numeric(
        df["ALLOCATION"],
        errors="coerce"
    ).fillna(0)

    df["Main_Allocation"] = pd.to_numeric(
        df["Main_Allocation"],
        errors="coerce"
    ).fillna(0)

    return df.reset_index(drop=True)
