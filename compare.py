"""
compare.py
-----------------------------------
Contains all comparison logic.
"""

import pandas as pd
from formatter import format_allocation

# Jainam allocation values are expressed in lakhs: 0.8 = ₹80,000 and 4 = ₹4,00,000.
JAINAM_ALLOCATION_UNIT = 100_000


def compare_allocations(df):
    """
    Compare:
    Expected Allocation = ALLOCATION × 10000
    with
    Main Allocation
    """

    # Work on a copy
    df = df.copy()

    # =====================================
    # Calculate Expected Allocation
    # =====================================

    df["Expected_Allocation"] = df["ALLOCATION"] * JAINAM_ALLOCATION_UNIT

    # =====================================
    # Match Status
    # =====================================

    df["Matched"] = (
        df["Expected_Allocation"] ==
        df["Main_Allocation"]
    )

    active_df = df[
        df["ALLOCATION"]
        .fillna(0)
        .astype(float)
        .ne(0)
    ].copy()

    # =====================================
    # KPI Values
    # =====================================

    total_users = len(df)

    active_users = len(active_df)

    matched_users = int(active_df["Matched"].sum())

    mismatch_users = active_users - matched_users

    # =====================================
    # Create Mismatch Table
    # =====================================

    mismatch_df = active_df[active_df["Matched"] == False].copy()

    mismatch_df = mismatch_df[
        [
            "UserID",
            "Expected_Allocation",
            "Main_Allocation",
        ]
    ]

    # =====================================
    # Format Allocation
    # =====================================

    mismatch_df["Expected_Allocation"] = (
        mismatch_df["Expected_Allocation"]
        .apply(format_allocation)
    )

    mismatch_df["Main_Allocation"] = (
        mismatch_df["Main_Allocation"]
        .apply(format_allocation)
    )

    # =====================================
    # Rename Columns
    # =====================================

    mismatch_df = mismatch_df.rename(
        columns={
            "UserID": "User ID",
            "Expected_Allocation": "Jainam Allocation",
            "Main_Allocation": "Main Allocation"
        }
    )

    # =====================================
    # Return Everything
    # =====================================

    return {
        "total_users": total_users,
        "active_users": active_users,
        "matched_users": matched_users,
        "mismatch_users": mismatch_users,
        "mismatch_df": mismatch_df
    }
