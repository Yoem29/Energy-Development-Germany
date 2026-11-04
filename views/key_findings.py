import streamlit as st

from config import START_YEAR, END_YEAR
from dashboard_charts import line_chart, delta_bar_chart
from dashboard_data import yearly, period_sum, SOURCES
from dashboard_layout import get_data, REPO_URL

df_all, df = get_data()
df = df[(df["Year"] >= START_YEAR) & (df["Year"] <= END_YEAR)]
df_yearly = yearly(df)
df_yearly["Coal"] = df_yearly["Lignite"] + df_yearly["Hard Coal"]
#The findings refer to the observation period of the analysis, so they stay the same when new years are added

st.title("💡 Key Findings")
st.markdown(
    f"Answers to the three research questions of the analysis ({START_YEAR} - {END_YEAR}). "
    f"The full analysis with all steps can be found in the [analysis notebook]({REPO_URL}/blob/main/notebooks/Analysis.ipynb)."
)

st.header("1. Renewable vs. Conventional")
st.markdown(
    "Renewable energy is the rising producer over the years. It overtook conventional energy in 2023 right around "
    "the time of the nuclear phase-out. In 2015, the share of renewable energy was at 33.8%. In 2025, the share was at 58.9%."
)
st.plotly_chart(line_chart(df_yearly, ["Renewable Share [%]", "Conventional Share [%]"],
                           "Share of renewable and conventional energy", y_label="Share [%]"))

st.header("2. Nuclear phase-out")
st.markdown(
    "The loss of nuclear energy after the phase-out was compensated through onshore wind and natural gas. "
    "The total energy production was still lower because the production through coal decreased as well. "
    "Imports are not included in the data set. But according to "
    "[Fraunhofer ISE](https://www.ise.fraunhofer.de/de/presse-und-medien/presseinformationen/2024/oeffentliche-stromerzeugung-2023-erneuerbare-energien-decken-erstmals-grossteil-des-stromverbrauchs.html), "
    "imports have increased at that time which might explain the gap."
)
before = period_sum(df, "2022-05-01", "2023-05-01")
after = period_sum(df, "2023-05-01", "2024-05-01")
differences = (after - before)[SOURCES]
#12 months before vs. 12 months after the phase-out, so seasonal effects are balanced out (see analysis, chapter 2.2)

col1, col2, col3 = st.columns(3)
col1.metric("Nuclear energy", f"{differences['Nuclear']:+.1f} TWh", border=True)
col2.metric("All increases together", f"{differences[differences > 0].sum():+.1f} TWh", border=True)
col3.metric("Coal (lignite + hard coal)", f"{differences['Lignite'] + differences['Hard Coal']:+.1f} TWh", border=True)
st.plotly_chart(delta_bar_chart(differences, "Change in energy production: 12 months after vs. before the nuclear phase-out"))

st.header("3. Energy crisis & coal")
st.markdown(
    "Energy from coal had a temporary increase from 2021 onwards with a peak in 2022 in which it had a share of 33.3% "
    "of the total energy production. In 2021, renewable energy had a weak year and the recovery from the corona pandemic "
    "also began. Even though the rise of coal peaked in 2022, renewable energy still had a greater growth in that year."
)
st.plotly_chart(line_chart(df_yearly, ["Coal", "Lignite", "Hard Coal", "Natural Gas"], "Energy production from coal and gas"))
st.plotly_chart(line_chart(df_yearly, ["Coal Share [%]"], "Share of coal in the total energy production", y_label="Share [%]"))

st.header(f"4. Outlook {END_YEAR}")
st.markdown(
    "For 2025, coal has its lowest share in the observed period of only 21.8%. "
    "The share of renewable energy is still increasing, but the growth has slowed down."
)
col1, col2 = st.columns(2)
col1.metric(f"Share of coal {END_YEAR}", f"{df_yearly.loc[END_YEAR, 'Coal Share [%]']:.1f}%",
            f"{df_yearly.loc[END_YEAR, 'Coal Share [%]'] - df_yearly.loc[END_YEAR - 1, 'Coal Share [%]']:+.1f} pp vs. {END_YEAR - 1}",
            delta_color="inverse", border=True)
col2.metric(f"Share of renewable energy {END_YEAR}", f"{df_yearly.loc[END_YEAR, 'Renewable Share [%]']:.1f}%",
            f"{df_yearly.loc[END_YEAR, 'Renewable Share [%]'] - df_yearly.loc[END_YEAR - 1, 'Renewable Share [%]']:+.1f} pp vs. {END_YEAR - 1}",
            border=True)
