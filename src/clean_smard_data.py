from pathlib import Path

import pandas as pd

from config import ENERGY_COLUMNS, EXPORT_TRANSLATION, START_YEAR, END_YEAR

DATA_PATH = Path(__file__).resolve().parent.parent / "data"
RAW_API_PATH = DATA_PATH / "raw" / "smard_generation_monthly.csv"
PROCESSED_PATH = DATA_PATH / "processed" / "energy_generation_clean.csv"


def add_derived_columns(df):
    for col in ENERGY_COLUMNS:
        twh_col = col.replace("[MWh]", "[TWh]")
        df[twh_col] = df[col] / 1_000_000
    #for visualization purposes later on, energy columns get duplicated with [TWh] instead of [MWh]

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month_name()
    #New columns for year and month (English month names)

    twh_columns = [col.replace("[MWh]", "[TWh]") for col in ENERGY_COLUMNS]
    df = df[["Date", "Year", "Month"] + ENERGY_COLUMNS + twh_columns]
    #New Columns are moved to the front

    return df


def clean_smard_export(filepath: str):
    #Cleans a csv-file that was downloaded manually from smard.de
    df = pd.read_csv(filepath, sep=";", na_values=["-"]) #read csv-file in a dataframe
    df.columns = df.columns.str.replace("Berechnete Auflösungen", "", regex=False).str.strip() #clean column names

    unknown_columns = [col for col in df.columns if "[MWh]" in col and col not in EXPORT_TRANSLATION]
    if unknown_columns:
        print("Warning: no English translation for these columns:", unknown_columns)
    df = df.rename(columns=EXPORT_TRANSLATION)
    #German column names translated to English. Unknown columns (e.g. a different SMARD export) are reported

    for col in ENERGY_COLUMNS:
        df[col] = (
           df[col]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
    #Numbers in the thousands use "." (e.x. 1.000,50) -> initial "." dropped, "," replaced with new "." for decimals

    df["Nuclear [MWh]"] = df["Nuclear [MWh]"].fillna(0)
    #Germany stopped using nuclear energy after 15.04.2023 which is why SMARD uses "-" to label the months after.
    #To keep it numeric, "-" labeled as "na-Value" (see above) and replaced with "0" here

    df["Date"] = pd.to_datetime(df["Datum von"], format="%d.%m.%Y")
    df = df.drop(columns=["Datum von", "Datum bis"])
    #2 columns with dates -> "from" and "until" (beginning and end of the month)
    #Start of the month will be kept as "Date". Column with end date dropped

    return add_derived_columns(df)


def clean_smard_api(filepath: str):
    #Cleans the csv-file created by fetch_smard_data.py. Numbers are already numeric, column names already English
    df = pd.read_csv(filepath, parse_dates=["Date"])

    df["Nuclear [MWh]"] = df["Nuclear [MWh]"].fillna(0)
    #The API has no nuclear values after 2023 (phase-out) -> replaced with "0" like in the export

    df = df.dropna(subset=ENERGY_COLUMNS).reset_index(drop=True)
    #Months that are not published yet have no values and are dropped

    return add_derived_columns(df)


if __name__ == "__main__":
    df = clean_smard_api(RAW_API_PATH)
    df = df[(df["Year"] >= START_YEAR) & (df["Year"] <= END_YEAR)]
    #Only the observation period of the analysis is saved
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Saved {len(df)} months ({START_YEAR} - {END_YEAR}) to {PROCESSED_PATH}")
