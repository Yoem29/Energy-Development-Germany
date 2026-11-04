#Data preparation for the dashboard (plain pandas, no Streamlit code)
import pandas as pd

from clean_smard_data import clean_smard_api, RAW_API_PATH
from config import SMARD_FILTERS, RENEWABLE_SOURCES, CONVENTIONAL_SOURCES

SOURCES = list(SMARD_FILTERS)
GROUPS = ["Renewable", "Conventional"]


def load_monthly_data():
    #All published months from the API data. Values in TWh, columns named after the energy source (e.g. "Lignite")
    df = clean_smard_api(RAW_API_PATH)
    df = df[["Date", "Year", "Month"] + [f"{source} [TWh]" for source in SOURCES]]
    df.columns = ["Date", "Year", "Month"] + SOURCES

    df["Renewable"] = df[RENEWABLE_SOURCES].sum(axis=1)
    df["Conventional"] = df[CONVENTIONAL_SOURCES].sum(axis=1)
    df["Total"] = df["Renewable"] + df["Conventional"]
    return df


def complete_years(df):
    #Only years with all 12 months published. A new year shows up automatically once its December is available
    months_per_year = df.groupby("Year")["Date"].count()
    years = months_per_year[months_per_year == 12].index
    return df[df["Year"].isin(years)]


def yearly(df):
    df_yearly = df.groupby("Year")[SOURCES + GROUPS + ["Total"]].sum()
    df_yearly["Renewable Share [%]"] = df_yearly["Renewable"] / df_yearly["Total"] * 100
    df_yearly["Conventional Share [%]"] = df_yearly["Conventional"] / df_yearly["Total"] * 100
    df_yearly["Coal Share [%]"] = (df_yearly["Lignite"] + df_yearly["Hard Coal"]) / df_yearly["Total"] * 100
    return df_yearly


def period_sum(df, start: str, end: str):
    #Sum of every energy source for all months from start (inclusive) to end (exclusive)
    period = df[(df["Date"] >= start) & (df["Date"] < end)]
    return period[SOURCES + GROUPS + ["Total"]].sum()
