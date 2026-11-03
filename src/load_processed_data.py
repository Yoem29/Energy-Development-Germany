import pandas as pd

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def load_data(filepath: str):
    df = pd.read_csv(filepath)
    df["Month"] = pd.Categorical(df["Month"], categories=MONTH_ORDER, ordered=True)
    return df
