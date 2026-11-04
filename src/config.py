#Central definitions for all scripts and notebooks, so energy sources and column names only exist in one place

#SMARD filter IDs for the realized electricity generation per energy source (used for the API requests)
SMARD_FILTERS = {
    "Biomass": 4066,
    "Hydropower": 1226,
    "Wind Offshore": 1225,
    "Wind Onshore": 4067,
    "Photovoltaics": 4068,
    "Other Renewables": 1228,
    "Nuclear": 1224,
    "Lignite": 1223,
    "Hard Coal": 4069,
    "Natural Gas": 4071,
    "Pumped Storage": 4070,
    "Other Conventional": 1227,
}

RENEWABLE_SOURCES = ["Biomass", "Hydropower", "Wind Offshore", "Wind Onshore", "Photovoltaics", "Other Renewables"]
CONVENTIONAL_SOURCES = ["Nuclear", "Lignite", "Hard Coal", "Natural Gas", "Pumped Storage", "Other Conventional"]
#Pumped storage counts as conventional for simplicity (see README, Limitations)

ENERGY_COLUMNS = [f"{source} [MWh]" for source in SMARD_FILTERS]
RENEWABLE_COLUMNS = [f"{source} [MWh]" for source in RENEWABLE_SOURCES]
CONVENTIONAL_COLUMNS = [f"{source} [MWh]" for source in CONVENTIONAL_SOURCES]

ENERGY_COLUMNS_TWH = [col.replace("[MWh]", "[TWh]") for col in ENERGY_COLUMNS]
RENEWABLE_COLUMNS_TWH = [col.replace("[MWh]", "[TWh]") for col in RENEWABLE_COLUMNS]
CONVENTIONAL_COLUMNS_TWH = [col.replace("[MWh]", "[TWh]") for col in CONVENTIONAL_COLUMNS]

#German column names of the manual SMARD csv export -> English names used in this project
EXPORT_TRANSLATION = {
    "Biomasse [MWh]": "Biomass [MWh]",
    "Wasserkraft [MWh]": "Hydropower [MWh]",
    "Wind Offshore [MWh]": "Wind Offshore [MWh]",
    "Wind Onshore [MWh]": "Wind Onshore [MWh]",
    "Photovoltaik [MWh]": "Photovoltaics [MWh]",
    "Sonstige Erneuerbare [MWh]": "Other Renewables [MWh]",
    "Kernenergie [MWh]": "Nuclear [MWh]",
    "Braunkohle [MWh]": "Lignite [MWh]",
    "Steinkohle [MWh]": "Hard Coal [MWh]",
    "Erdgas [MWh]": "Natural Gas [MWh]",
    "Pumpspeicher [MWh]": "Pumped Storage [MWh]",
    "Sonstige Konventionelle [MWh]": "Other Conventional [MWh]",
}

#Observation period of the analysis. The API delivers more data, but only complete years in this range are processed
START_YEAR = 2015
END_YEAR = 2025

#Dashboard: fixed colors, so every energy source looks the same in all charts
ENERGY_COLORS = {
    "Biomass": "#6a994e",
    "Hydropower": "#1f77b4",
    "Wind Offshore": "#08306b",
    "Wind Onshore": "#6baed6",
    "Photovoltaics": "#f2b705",
    "Other Renewables": "#b5d99c",
    "Nuclear": "#9467bd",
    "Lignite": "#8c564b",
    "Hard Coal": "#3d3d3d",
    "Natural Gas": "#ff7f0e",
    "Pumped Storage": "#17becf",
    "Other Conventional": "#bdbdbd",
}
GROUP_COLORS = {"Renewable": "#2ca02c", "Conventional": "#7f7f7f"}

#Dashboard: events marked in the charts
EVENTS = [
    ("2020-03-01", "Corona pandemic"),
    ("2020-08-01", "Coal phase-out law"),
    ("2022-01-01", "3 nuclear reactors shut down"),
    ("2022-02-24", "Energy crisis (Russia-Ukraine war)"),
    ("2023-04-15", "Nuclear phase-out"),
]
#Monthly charts use the exact dates above. Yearly charts highlight the whole year instead
EVENT_YEARS = {
    2020: "Corona & coal phase-out law",
    2022: "Energy crisis",
    2023: "Nuclear phase-out",
}
