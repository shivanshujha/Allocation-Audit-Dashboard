"""
app.py
---------------------------------------
Allocation Audit Dashboard
"""

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from google_sheet import load_jainam_data
from compare import compare_allocations
from utils import get_last_refresh, create_excel

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Allocation Audit Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* Reduce white space */
.block-container{
    padding-top:0.3rem;
    padding-bottom:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* Remove Streamlit menu/footer */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* KPI Cards */
[data-testid="stMetric"]{
    background:#f8f9fa;
    border:1px solid #d9d9d9;
    padding:12px;
    border-radius:10px;
    text-align:center;
    margin-bottom:12px;
}

/* Table Header */
thead tr th{
    background:#8B0000 !important;
    color:white !important;
    font-weight:bold !important;
    text-align:center !important;
}

/* Table Cells */
tbody tr td{
    text-align:center !important;
    font-weight:bold !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================

# ==========================================================
# HEADER
# ==========================================================

st.title("📊 Allocation Audit Dashboard")

st.caption(
    f"Last Refresh : {get_last_refresh()}  |  Auto Refresh : Every 30 Seconds"
)

st.divider()

# ==========================================================
# LOAD DATA
# ==========================================================

with st.spinner("Loading latest data..."):

    df = load_jainam_data()

results = compare_allocations(df)

# ==========================================================
# TABLE + KPI
# ==========================================================

left, right = st.columns([4,1])

# ==========================================================
# LEFT
# ==========================================================

with left:

    st.subheader("❌ Allocation Mismatch Users")

    if results["mismatch_df"].empty:

        st.success("🎉 All Users Matched")

    else:

        styled = (
            results["mismatch_df"]
            .style
            .hide(axis="index")

            # Whole table
            .set_properties(**{
                "background-color":"#A30000",
                "color":"white",
                "font-weight":"bold",
                "text-align":"center"
            })

            # User ID Bigger
            .set_properties(
                subset=["User ID"],
                **{
                    "font-size":"18px",
                    "font-weight":"900"
                }
            )

            # Allocation Font
            .set_properties(
                subset=[
                    "Jainam Allocation",
                    "Main Allocation"
                ],
                **{
                    "font-size":"15px"
                }
            )
        )

        st.dataframe(results["mismatch_df"], use_container_width=True)

# ==========================================================
# RIGHT KPI
# ==========================================================

with right:

    st.metric(
        "👥 Total Users",
        results["total_users"]
    )

    st.metric(
        "✅ Matched",
        results["matched_users"]
    )

    st.metric(
        "❌ Mismatch",
        results["mismatch_users"]
    )

    st.metric(
        "📈 Match %",
        f"{results['match_percentage']}%"
    )

# ==========================================================
# DOWNLOAD
# ==========================================================

st.divider()

excel = create_excel(results["mismatch_df"])

st.download_button(
    "📥 Download Mismatch Report",
    data=excel,
    file_name="Mismatch_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)