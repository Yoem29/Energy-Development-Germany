import pandas as pd

MONATE_REIHENFOLGE = [
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember"
]

def load_data(filepath: str):
    df = pd.read_csv(filepath)
    df["Monat"] = pd.Categorical(df["Monat"], categories=MONATE_REIHENFOLGE, ordered=True)
    return df