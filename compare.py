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

    # An allocation of 0.0 represents an inactive user. Keep the full user
    # totals unchanged, but expose an active-user KPI separately.
    active_df = df[df["ALLOCATION"] != 0].copy()

    # =====================================
    # KPI Values
    # =====================================

    total_users = len(df)

    active_users = len(active_df)

    matched_users = int(df["Matched"].sum())

    mismatch_users = total_users - matched_users

    match_percentage = (
        round((matched_users / total_users) * 100, 2)
        if total_users
        else 0
    )

    # =====================================
    # Create Mismatch Table
    # =====================================

    mismatch_df = df[df["Matched"] == False].copy()

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
        "match_percentage": match_percentage,
        "mismatch_df": mismatch_df
    }
