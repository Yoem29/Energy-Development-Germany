import streamlit as st

from dashboard_charts import line_chart, stacked_area_chart
from dashboard_data import yearly
from dashboard_layout import get_data

df_all, df = get_data()
df_yearly = yearly(df)
latest_year = df_yearly.index.max()
previous_year = latest_year - 1

st.title("⚡ Energy Development Germany")
st.markdown(
    f"How has Germany's electricity production developed between {df_yearly.index.min()} and {latest_year}? "
    "This dashboard shows the realized electricity generation of the public grid, based on official data from SMARD. "
    "Use the **Explorer** to filter the data yourself, or read the answers to the research questions in **Key Findings**."
)

st.subheader(f"{latest_year} at a glance")
col1, col2, col3 = st.columns(3)
col1.metric(
    "Share of renewable energy",
    f"{df_yearly.loc[latest_year, 'Renewable Share [%]']:.1f}%",
    f"{df_yearly.loc[latest_year, 'Renewable Share [%]'] - df_yearly.loc[previous_year, 'Renewable Share [%]']:+.1f} pp vs. {previous_year}",
    border=True,
)
col2.metric(
    "Share of coal",
    f"{df_yearly.loc[latest_year, 'Coal Share [%]']:.1f}%",
    f"{df_yearly.loc[latest_year, 'Coal Share [%]'] - df_yearly.loc[previous_year, 'Coal Share [%]']:+.1f} pp vs. {previous_year}",
    delta_color="inverse",
    border=True,
)
col3.metric(
    "Total production",
    f"{df_yearly.loc[latest_year, 'Total']:.1f} TWh",
    f"{df_yearly.loc[latest_year, 'Total'] - df_yearly.loc[previous_year, 'Total']:+.1f} TWh vs. {previous_year}",
    delta_color="off",
    border=True,
)
#pp = percentage points. A falling coal share is shown in green (delta_color="inverse")

st.plotly_chart(line_chart(df_yearly, ["Renewable Share [%]", "Conventional Share [%]"],
                           "Share of renewable and conventional energy", y_label="Share [%]"))
st.plotly_chart(stacked_area_chart(df_yearly, ["Renewable", "Conventional"],
                                   "Energy production: renewable vs. conventional"))

st.caption("Highlighted years mark events that influenced the energy production. "
           "Only complete years are shown.")
