#Entry point of the dashboard. Run locally with: streamlit run app.py
import sys
from pathlib import Path

SRC_PATH = str(Path(__file__).resolve().parent / "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)
#The dashboard modules are in src/, like the scripts used by the notebooks

import streamlit as st

from dashboard_layout import get_data, sidebar_footer

st.set_page_config(page_title="Energy Development Germany", page_icon="⚡", layout="wide")

pages = [
    st.Page("views/overview.py", title="Overview", icon="📊", default=True),
    st.Page("views/explorer.py", title="Explorer", icon="🔎"),
    st.Page("views/key_findings.py", title="Key Findings", icon="💡"),
]
st.navigation(pages).run()

df_all, _ = get_data()
sidebar_footer(df_all)
#Shown in the sidebar of every page
