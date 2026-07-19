"""
utils.py
----------------------------------------
Helper functions used throughout the
Allocation Audit Dashboard.
"""

import io
import pandas as pd
from datetime import datetime


# ===================================================
# LAST REFRESH TIME
# ===================================================

def get_last_refresh():
    """
    Returns current system time.
    """

    return datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")


# ===================================================
# MATCH PERCENTAGE
# ===================================================

def calculate_match_percentage(matched, total):
    """
    Calculates match percentage.
    """

    if total == 0:
        return 0

    return round((matched / total) * 100, 2)


# ===================================================
# EXCEL DOWNLOAD
# ===================================================

def create_excel(df):
    """
    Creates an Excel report from the mismatch dataframe.
    """

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        df.to_excel(
            writer,
            sheet_name="Mismatch Users",
            index=False
        )

    output.seek(0)

    return output