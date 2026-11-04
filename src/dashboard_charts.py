#Plotly charts for the dashboard. Every function returns a figure that the pages show with st.plotly_chart()
import pandas as pd
import plotly.graph_objects as go

from config import ENERGY_COLORS, GROUP_COLORS, EVENTS, EVENT_YEARS

COLORS = {**ENERGY_COLORS, **GROUP_COLORS, "Coal": "#5c3d2e"}


def color_for(name):
    #"Renewable Share [%]" gets the color of "Renewable", "Coal Share [%]" the color of "Coal" etc.
    return COLORS.get(name, COLORS.get(name.split(" ")[0]))


def add_events(fig, x_is_year: bool, x_min=None, x_max=None):
    #Yearly charts: the whole event year gets highlighted. Monthly charts: a dotted line at the exact date
    if x_is_year:
        for i, (year, label) in enumerate(EVENT_YEARS.items()):
            if x_min is not None and not (x_min <= year <= x_max):
                continue
            fig.add_vrect(x0=year - 0.45, x1=year + 0.45, fillcolor="grey", opacity=0.12, line_width=0)
            fig.add_annotation(x=year, y=1 + (i % 2) * 0.07, yref="paper", text=label, showarrow=False,
                               yanchor="bottom", font_size=11)
    else:
        for i, (date, label) in enumerate(EVENTS):
            date = pd.Timestamp(date)
            if x_min is not None and not (x_min <= date <= x_max):
                continue
            fig.add_vline(x=date, line_dash="dot", line_color="grey")
            fig.add_annotation(x=date, y=1 + (i % 2) * 0.07, yref="paper", text=label, showarrow=False,
                               xanchor="left", yanchor="bottom", font_size=11)
    #Labels alternate in height, so events close to each other don't overlap
    return fig


def line_chart(df, columns, title, y_label="Energy production [TWh]", x_is_year=True, events=True):
    fig = go.Figure()
    for col in columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col, mode="lines+markers" if x_is_year else "lines",
                                 line_color=color_for(col)))
    if events:
        add_events(fig, x_is_year, df.index.min(), df.index.max())
    fig.update_layout(title=title, yaxis_title=y_label, hovermode="x unified", margin_t=110)
    if x_is_year:
        fig.update_xaxes(dtick=1)
    return fig


def stacked_area_chart(df, columns, title, y_label="Energy production [TWh]", x_is_year=True):
    fig = go.Figure()
    for col in columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col, stackgroup="one", line_color=color_for(col)))
    add_events(fig, x_is_year, df.index.min(), df.index.max())
    fig.update_layout(title=title, yaxis_title=y_label, hovermode="x unified", margin_t=110)
    if x_is_year:
        fig.update_xaxes(dtick=1)
    return fig


def ranking_bar_chart(values: pd.Series, title):
    values = values.sort_values()
    fig = go.Figure(go.Bar(x=values, y=values.index, orientation="h",
                           marker_color=[color_for(source) for source in values.index],
                           text=values.round(1), textposition="outside"))
    fig.update_layout(title=title, xaxis_title="Energy production [TWh]", showlegend=False)
    return fig


def delta_bar_chart(differences: pd.Series, title):
    differences = differences.sort_values()
    colors = ["#d62728" if diff < 0 else "#2ca02c" for diff in differences]
    fig = go.Figure(go.Bar(x=differences, y=differences.index, orientation="h", marker_color=colors,
                           text=differences.round(1), textposition="outside"))
    fig.add_vline(x=0, line_color="black", line_width=1)
    fig.update_layout(title=title, xaxis_title="Difference [TWh]", showlegend=False)
    return fig


def share_donut_chart(renewable, conventional, title):
    fig = go.Figure(go.Pie(labels=["Renewable", "Conventional"], values=[renewable, conventional], hole=0.5,
                           marker_colors=[GROUP_COLORS["Renewable"], GROUP_COLORS["Conventional"]],
                           sort=False, textinfo="label+percent"))
    fig.update_layout(title=title, showlegend=False)
    return fig
