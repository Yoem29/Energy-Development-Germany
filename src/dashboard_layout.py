#Streamlit parts that every dashboard page uses: cached data and the sidebar footer
import streamlit as st

from dashboard_data import load_monthly_data, complete_years

REPO_URL = "https://github.com/Yoem29/Energy-Development-Germany"


@st.cache_data
def get_data():
    #Cached, so the csv-file is only read once and not on every click
    df_all = load_monthly_data()
    return df_all, complete_years(df_all)


def sidebar_footer(df_all):
    st.sidebar.caption(f"Data as of: {df_all['Date'].max():%B %Y}")
    st.sidebar.caption("Source: [SMARD](https://www.smard.de) (Bundesnetzagentur), license CC BY 4.0")
    st.sidebar.caption(f"Code & analysis: [GitHub]({REPO_URL})")
