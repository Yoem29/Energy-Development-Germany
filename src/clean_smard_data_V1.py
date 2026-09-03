import pandas as pd

def clean_smard_erzeugung(filepath: str):
    df = pd.read_csv(filepath, sep=";", na_values=["-"]) #read csv-file in a dataframe
    df.columns = df.columns.str.replace("Berechnete Auflösungen", "", regex=False).str.strip() #clean column names


    energy_columns = [
        "Biomasse [MWh]", "Wasserkraft [MWh]", "Wind Offshore [MWh]", "Wind Onshore [MWh]", "Photovoltaik [MWh]",
        "Sonstige Erneuerbare [MWh]", "Kernenergie [MWh]", "Braunkohle [MWh]", "Steinkohle [MWh]", "Erdgas [MWh]",
        "Pumpspeicher [MWh]", "Sonstige Konventionelle [MWh]"
    ]

    for col in energy_columns:
        df[col] = (
           df[col]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce") 

    #Numbers in the thousands use "." (e.x. 1.000,50) -> initial "." dropped, "," replaced with new "." for decimals

    df["Kernenergie [MWh]"] = df["Kernenergie [MWh]"].fillna(0)
    #Germany stopped using nuclear energy after 15.04.2023 which is why SMARD uses "-" to label the months after.
    #To keep it numeric, "-" labeled as "na-Value" (see above) and replaced with "0" here

    df["Datum von"] = pd.to_datetime(df["Datum von"], format="%d.%m.%Y")
    df["Jahr"] = df["Datum von"].dt.year
    #New column for year only

    monate_de = {
        1: "Januar", 2: "Februar", 3: "März", 4: "April",
        5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
        9: "September", 10: "Oktober", 11: "November", 12: "Dezember"
    }
    df["Monat"] = df["Datum von"].dt.month.map(monate_de)
    #New column for months
    #Numbers replaced with name of the months

    df = df.drop(columns=["Datum bis"])
    #2 columns with dates -> "from" and "until" (beginning and end of the month)
    #Start of the month will be kept. Column with end date dropped

    return df