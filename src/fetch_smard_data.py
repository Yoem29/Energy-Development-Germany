from pathlib import Path

import pandas as pd
import requests

from config import SMARD_FILTERS

BASE_URL = "https://www.smard.de/app/chart_data"
RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "smard_generation_monthly.csv"


def fetch_series(filter_id: int, region: str = "DE", resolution: str = "month"):
    #SMARD splits the data into blocks. Step 1: get the start timestamps of all available blocks
    index_url = f"{BASE_URL}/{filter_id}/{region}/index_{resolution}.json"
    response = requests.get(index_url, timeout=30)
    response.raise_for_status()
    timestamps = response.json()["timestamps"]

    #Step 2: download every block. Each block contains pairs of [timestamp, value in MWh]
    values = []
    for timestamp in timestamps:
        data_url = f"{BASE_URL}/{filter_id}/{region}/{filter_id}_{region}_{resolution}_{timestamp}.json"
        response = requests.get(data_url, timeout=30)
        response.raise_for_status()
        values += response.json()["series"]

    series = pd.Series(dict(values), dtype="float64")
    series.index = pd.to_datetime(series.index, unit="ms", utc=True).tz_convert("Europe/Berlin").tz_localize(None)
    #Timestamps are in milliseconds (UTC). Converted to German time, so every value starts at the first day of the month
    return series


def fetch_generation():
    df = pd.DataFrame({f"{source} [MWh]": fetch_series(filter_id) for source, filter_id in SMARD_FILTERS.items()})
    df.index.name = "Date"
    return df.sort_index()
    #Months that are not published yet (or nuclear after 2023) stay empty (NaN). They get handled in clean_smard_data.py


if __name__ == "__main__":
    df = fetch_generation()
    df.to_csv(RAW_PATH)
    print(f"Saved {len(df)} months ({df.index.min():%Y-%m} to {df.index.max():%Y-%m}) to {RAW_PATH}")
