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
