import streamlit as st

from dashboard_charts import line_chart, ranking_bar_chart, delta_bar_chart, share_donut_chart
from dashboard_data import yearly, SOURCES, GROUPS
from dashboard_layout import get_data

df_all, df = get_data()
df_yearly = yearly(df)
years = list(df_yearly.index)

st.title("🔎 Explorer")
st.markdown("Choose the time view and the energy sources in the sidebar. All values in TWh.")

#Sidebar filters
view = st.sidebar.radio("Time view", ["Years", "Months of a year"])
selected_year = st.sidebar.selectbox("Year (for months, ranking and share)", years[::-1])
grouping = st.sidebar.radio("Show", ["Renewable vs. Conventional", "Individual energy sources"])
if grouping == "Individual energy sources":
    columns = st.sidebar.multiselect("Energy sources", SOURCES, default=["Lignite", "Hard Coal", "Natural Gas", "Wind Onshore", "Photovoltaics", "Nuclear"])
else:
    columns = GROUPS

tab_development, tab_ranking, tab_share, tab_comparison = st.tabs(["Development", "Ranking", "Share", "Comparison"])

with tab_development:
    if not columns:
        st.info("Please select at least one energy source in the sidebar.")
    elif view == "Years":
        st.plotly_chart(line_chart(df_yearly, columns, "Yearly energy production"))
    else:
        df_months = df[df["Year"] == selected_year].set_index("Date")
        st.plotly_chart(line_chart(df_months, columns, f"Monthly energy production {selected_year}", x_is_year=False))

with tab_ranking:
    ranking_sources = columns if grouping == "Individual energy sources" and columns else SOURCES
    st.plotly_chart(ranking_bar_chart(df_yearly.loc[selected_year, ranking_sources], f"Energy production by source {selected_year}"))

with tab_share:
    col_chart, col_numbers = st.columns([2, 1])
    renewable = df_yearly.loc[selected_year, "Renewable"]
    conventional = df_yearly.loc[selected_year, "Conventional"]
    col_chart.plotly_chart(share_donut_chart(renewable, conventional, f"Share of the total production {selected_year}"))
    col_numbers.metric("Renewable", f"{renewable:.1f} TWh", border=True)
    col_numbers.metric("Conventional", f"{conventional:.1f} TWh", border=True)
    col_numbers.metric("Total", f"{renewable + conventional:.1f} TWh", border=True)

with tab_comparison:
    col_a, col_b = st.columns(2)
    year_a = col_a.selectbox("From year", years, index=years.index(years[-2]) if len(years) > 1 else 0)
    year_b = col_b.selectbox("To year", years, index=len(years) - 1)

    differences = df_yearly.loc[year_b, SOURCES] - df_yearly.loc[year_a, SOURCES]

    col1, col2, col3 = st.columns(3)
    for col, name in zip([col1, col2, col3], ["Renewable", "Conventional", "Total"]):
        col.metric(f"{name} {year_b}", f"{df_yearly.loc[year_b, name]:.1f} TWh",
                   f"{df_yearly.loc[year_b, name] - df_yearly.loc[year_a, name]:+.1f} TWh vs. {year_a}",
                   delta_color={"Renewable": "normal", "Conventional": "inverse", "Total": "off"}[name], border=True)
    #Less conventional energy is shown in green, more renewable energy as well
    st.plotly_chart(delta_bar_chart(differences, f"Change in energy production: {year_b} vs. {year_a}"))
