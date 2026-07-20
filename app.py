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

st.title("📊 Allocation Audit Dashboard")

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
# KPI + TABLE
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#E3F2FD,#BBDEFB);
    padding:22px;
    border-radius:16px;
    border-left:8px solid #1565C0;
    box-shadow:0 4px 14px rgba(21,101,192,0.18);">
    <h5 style="margin:0;color:#0D47A1;">👥 Total Users</h5>
    <h2 style="margin:8px 0 0;color:#0D47A1;">{results['total_users']}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#E8F5E9,#C8E6C9);
    padding:22px;
    border-radius:16px;
    border-left:8px solid #2E7D32;
    box-shadow:0 4px 14px rgba(46,125,50,0.18);">
    <h5 style="margin:0;color:#1B5E20;">🟢 Today's Active Users</h5>
    <h2 style="margin:8px 0 0;color:#1B5E20;">{results['active_users']}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#FFF8E1,#FFE0B2);
    padding:22px;
    border-radius:16px;
    border-left:8px solid #EF6C00;
    box-shadow:0 4px 14px rgba(239,108,0,0.18);">
    <h5 style="margin:0;color:#E65100;">✅ Matched Users</h5>
    <h2 style="margin:8px 0 0;color:#E65100;">{results['matched_users']}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#FDECEA,#FFCDD2);
    padding:22px;
    border-radius:16px;
    border-left:8px solid #C62828;
    box-shadow:0 4px 14px rgba(198,40,40,0.18);">
    <h5 style="margin:0;color:#B71C1C;">❌ Mismatch Users</h5>
    <h2 style="margin:8px 0 0;color:#B71C1C;">{results['mismatch_users']}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

# ==========================================================
# TABLE
# ==========================================================

st.subheader("❌ Allocation Mismatch Users")

if results["mismatch_df"].empty:

    st.success("🎉 All Users Matched")

else:

    st.warning("⚠️ Check allocation of below user.")

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

        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("font-weight", "900"),
                    ("text-align", "center"),
                ],
            }
        ])
    )

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
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
