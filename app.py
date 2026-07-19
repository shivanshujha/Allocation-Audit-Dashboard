"""Allocation Audit Dashboard."""

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from compare import compare_allocations
from google_sheet import load_jainam_data
from utils import get_last_refresh


st.set_page_config(page_title="Allocation Audit Dashboard", page_icon="📊", layout="wide")
st_autorefresh(interval=30_000, key="allocation_refresh")

st.markdown(
    """
    <style>
        .block-container { padding-top: 0.35rem; }
        h1 {
            color: #0b1f3a;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        h3 { color: #a40000; font-weight: 800; }
        [data-testid="stMetric"] {
            background: linear-gradient(145deg, #102a43, #1c4d72);
            border: 2px solid #ffd166;
            border-radius: 12px;
            padding: 14px 12px;
            margin-bottom: 12px;
            box-shadow: 0 5px 12px rgba(11, 31, 58, 0.22);
        }
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-weight: 800 !important;
        }
        [data-testid="stMetricLabel"] { font-size: 1rem !important; }
        [data-testid="stMetricValue"] { font-size: 2rem !important; }
        [data-testid="stCaptionContainer"] { color: #52616b; font-weight: 600; }
        .mismatch-kpi {
            background: linear-gradient(145deg, #8b0000, #c1121f);
            border: 2px solid #ffccd5;
            border-radius: 12px;
            box-shadow: 0 6px 14px rgba(139, 0, 0, 0.35);
            color: #ffffff;
            margin-bottom: 12px;
            padding: 14px 12px;
            text-align: center;
        }
        .mismatch-kpi .label { font-size: 1.1rem; font-weight: 800; }
        .mismatch-kpi .value { font-size: 2.4rem; font-weight: 900; line-height: 1.2; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📊 Allocation Audit Dashboard")
st.caption(f"Auto-refresh: every 30 seconds · Last refresh: {get_last_refresh()}")

try:
    with st.spinner("Loading latest data…"):
        results = compare_allocations(load_jainam_data())
except Exception as exc:
    st.error(f"Unable to load allocation data: {exc}")
    st.stop()

table_column, kpi_column = st.columns([4, 1], vertical_alignment="top")

with table_column:
    st.subheader("Allocation mismatch users")
    st.warning("**Values below require allocation review.**", icon="⚠️")

    if results["mismatch_df"].empty:
        st.success("All users matched.")
    else:
        visible_mismatches = (
            results["mismatch_df"]
            .style
            .set_properties(
                **{
                    "color": "#243b53",
                    "background-color": "#f7fafc",
                    "font-weight": "700",
                    "font-size": "18px",
                    "text-align": "center",
                    "border": "1px solid #d9e2ec",
                }
            )
            .set_properties(
                subset=["User ID"],
                **{
                    "color": "#c1121f",
                    "font-weight": "900",
                    "font-size": "25px",
                    "background-color": "#fff0f0",
                    "border-left": "5px solid #c1121f",
                }
            )
            .set_properties(
                subset=["Jainam Allocation", "Main Allocation"],
                **{
                    "color": "#b54708",
                    "font-weight": "900",
                    "font-size": "23px",
                    "background-color": "#fff4e5",
                }
            )
            .set_table_styles(
                [
                    {
                        "selector": "th",
                        "props": [
                            ("color", "#1f2933"),
                            ("background-color", "#ffffff"),
                            ("font-weight", "800"),
                            ("font-size", "20px"),
                            ("letter-spacing", "0.2px"),
                            ("padding", "10px 8px"),
                            ("text-align", "center"),
                            ("border", "1px solid #d9e2ec"),
                            ("border-bottom", "2px solid #9fb3c8"),
                        ],
                    },
                    {
                        "selector": "tbody tr:nth-child(even) td",
                        "props": [("background-color", "#eef4f9")],
                    },
                    {
                        "selector": "th.col_heading.level0.col0, th.col_heading.level0.col1, th.col_heading.level0.col2",
                        "props": [
                            ("font-weight", "900"),
                            ("text-shadow", "0 1px 1px rgba(0, 0, 0, 0.25)"),
                        ],
                    },
                ]
            )
        )
        st.markdown(
            visible_mismatches.hide(axis="index").to_html(), unsafe_allow_html=True
        )

with kpi_column:
    st.markdown(
        f"""
        <div class="mismatch-kpi">
            <div class="label">MISMATCHED</div>
            <div class="value">{results['mismatch_users']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.metric("Total users", results["total_users"])
    st.metric("Matched", results["matched_users"])
    st.metric("Total active", results["active_users"])
