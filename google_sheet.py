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
from pathlib import Path

# ==========================================
# GOOGLE API SCOPES
# ==========================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

PROJECT_DIR = Path(__file__).resolve().parent
SERVICE_ACCOUNT_FILE = PROJECT_DIR / "service_account.json"


# ==========================================
# GOOGLE CLIENT
# ==========================================

@st.cache_resource
def get_client():
    """
    Creates Google Sheets client.
    """

    # Streamlit raises when no secrets file exists, so read secrets defensively.
    # This keeps local runs independent of .streamlit/secrets.toml.
    try:
        service_account_info = st.secrets.get("gcp_service_account")
    except Exception:
        service_account_info = None

    # -------- Streamlit Cloud --------
    if service_account_info:

        creds = Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )

    # -------- Local Computer --------
    else:

        if not SERVICE_ACCOUNT_FILE.is_file():
            raise FileNotFoundError(
                "Google credentials file was not found. Expected it at "
                f"'{SERVICE_ACCOUNT_FILE}'. Add service_account.json there, "
                "or configure Streamlit secrets as gcp_service_account."
            )

        creds = Credentials.from_service_account_file(
            str(SERVICE_ACCOUNT_FILE),
            scopes=SCOPES
        )

    return gspread.authorize(creds)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data(ttl=30)
def load_jainam_data():
    """
    Loads Jainam worksheet every 30 seconds.
    """

    client = get_client()

    workbook = client.open("All User Details Daily Updated")

    worksheet = workbook.worksheet("Jainam")

    df = pd.DataFrame(worksheet.get_all_records())

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
