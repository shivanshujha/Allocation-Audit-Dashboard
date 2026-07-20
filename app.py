"""
app.py
---------------------------------------
Allocation Audit Dashboard
"""

import streamlit as st
import streamlit.components.v1 as components
from google_sheet import load_jainam_data
from compare import compare_allocations
from utils import get_last_refresh, create_excel

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Allocation Audit Dashboard",
    page_icon="ðŸ“Š",
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
# AUTO REFRESH
# ==========================================================

components.html(
    """
    <script>
    setTimeout(() => window.parent.location.reload(), 30000);
    </script>
    """,
    height=0,
)
# ==========================================================
# HEADER
# ==========================================================

st.title("ðŸ“Š Allocation Audit Dashboard")

st.caption(
    f"Last Refresh : {get_last_refresh()}  |  Auto Refresh : Every 30 Seconds"
)

st.divider()

# ==========================================================
# LOAD DATA
# ==========================================================
# LOAD DATA
# ==========================================================

results = None

try:

    with st.spinner("Loading latest data..."):
        df = load_jainam_data()
        st.success("Google Sheet loaded successfully")
    results = compare_allocations(df)

except Exception as e:

    st.error("Application Error")

    st.exception(e)

    st.stop()

    raise SystemExit(1)

# ==========================================================
# TABLE + KPI
# ==========================================================

left, right = st.columns([4,1])

# ==========================================================
# LEFT
# ==========================================================

with left:

    st.subheader("âŒ Allocation Mismatch Users")

    if results["mismatch_df"].empty:

        st.success("ðŸŽ‰ All Users Matched")

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

        st.dataframe(
            styled,
            use_container_width=True,
            hide_index=True,
        )


# ==========================================================
# RIGHT KPI
# ==========================================================

with right:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="
        background:#E3F2FD;
        padding:20px;
        border-radius:15px;
        border-left:8px solid #2196F3;">
        <h5>👥 Total Users</h5>
        <h2>{results['total_users']}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
        background:#E8F5E9;
        padding:20px;
        border-radius:15px;
        border-left:8px solid #4CAF50;">
        <h5>🟢 Active Users</h5>
        <h2>{results['active_users']}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
        background:#FFF8E1;
        padding:20px;
        border-radius:15px;
        border-left:8px solid #FF9800;">
        <h5>✅ Matched</h5>
        <h2>{results['matched_users']}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style="
        background:#FDECEA;
        padding:20px;
        border-radius:15px;
        border-left:8px solid #F44336;">
        <h5>❌ Mismatch</h5>
        <h2>{results['mismatch_users']}</h2>
        </div>
        """, unsafe_allow_html=True)
# ==========================================================
# DOWNLOAD
# ==========================================================

st.divider()

excel = create_excel(results["mismatch_df"])

st.download_button(
    "ðŸ“¥ Download Mismatch Report",
    data=excel,
    file_name="Mismatch_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
