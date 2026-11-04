# Energy Development Germany 2015–2025

> 🚧 Data pipeline and analysis are complete. The interactive Streamlit dashboard is currently in progress.

Showcase project analyzing the development of Germany's electricity production between 2015 and 2025, based on official data from SMARD (Bundesnetzagentur).

## Current Status

- ✅ Automated data retrieval via the SMARD API
- ✅ Data cleaning
- ✅ Exploratory Data Analysis (EDA)
- ✅ Analysis of all three research questions
- ⬜ Dashboard (planned, via Streamlit)

## Motivation

The transition toward renewable energy is a central topic in Germany's energy policy. This project examines how the country's electricity mix has actually developed over the past decade, and what role major events — such as the coal phase-out law, the 2022 energy crisis, and the final nuclear phase-out — played in that development.

## Research Questions

1. How has renewable energy production developed compared to conventional energy production?
2. What impact did the shutdown of nuclear energy (April 2023) have on other energy producers?
3. How did the 2022 energy crisis influence the temporary rise of coal-based energy production?

## Data Source

- **Provider:** [SMARD](https://www.smard.de) (Bundesnetzagentur / German Federal Network Agency)
- **Access:** Fetched automatically via the public SMARD API (`src/fetch_smard_data.py`). A manual csv export is kept as reference; both datasets were compared and match exactly for 2015–2025 (see EDA notebook, section 3).
- **Metric:** Realized (net) electricity generation, i.e. electricity actually fed into the public grid
- **Time range:** 2015–2025
- **Resolution:** Monthly
- **License:** CC BY 4.0

**Note on data scope:** The data reflects generation from the public electricity grid only. It does not include self-generated electricity consumed directly by industrial facilities, nor generation within closed distribution networks (e.g. Deutsche Bahn). It also excludes grid losses and the self-consumption of power plants. This is the standard scope used across most German energy statistics (SMARD, Destatis, Fraunhofer ISE) and remains consistent across the entire observation period.

## Project Structure

```
├── data/
│   ├── raw/            # SMARD data from the API + original manual export (reference)
│   └── processed/       # Cleaned data, ready for analysis
├── notebooks/
│   ├── EDA.ipynb         # Data cleaning walkthrough, API validation and first insights
│   └── Analysis.ipynb    # In-depth analysis of the research questions
├── src/
│   ├── config.py               # Energy sources, SMARD filter IDs, column names, observation period
│   ├── fetch_smard_data.py     # Downloads the monthly generation data from the SMARD API
│   ├── clean_smard_data.py     # Cleaning logic for API data and manual SMARD exports
│   └── load_processed_data.py  # Helper to load processed data with correct month ordering
├── requirements.txt
└── .gitignore
```

## Methodology

0. **Data retrieval** – The monthly generation data of all 12 energy sources is downloaded from the SMARD API and validated against a manual SMARD export.
1. **Cleaning** – Raw SMARD data (German number format, missing-value placeholders, German column names) is transformed into a consistent, analysis-ready dataset with English column names.
2. **EDA** – Initial exploration of the cleaned data: data types, value ranges, and first visible patterns (e.g. the nuclear phase-out showing up as a structural break).
3. **Analysis** – Each research question is examined individually, combining yearly trends with monthly detail where relevant.
4. **Dashboard** *(planned)* – An interactive Streamlit dashboard to explore the data and findings.

## Key Findings

Full analysis and charts: [`notebooks/Analysis.ipynb`](notebooks/Analysis.ipynb)

1. **Renewable vs Conventional:** Renewable energy is the rising producer over the years. It overtook conventional energy in 2023 right around the time of the nuclear phase-out. In 2015, the share of renewable energy was at 33.8%. In 2025, the share was at 58.9%.
2. **Nuclear phase-out:** The loss of nuclear energy after the phase-out was compensated through onshore wind and natural gas. The total energy production was still lower because the production through coal decreased as well. Imports are not included in the data set. But according to [Fraunhofer ISE](https://www.ise.fraunhofer.de/de/presse-und-medien/presseinformationen/2024/oeffentliche-stromerzeugung-2023-erneuerbare-energien-decken-erstmals-grossteil-des-stromverbrauchs.html), imports have increased at that time which might explain the gap.
3. **Energy crisis & coal:** Energy from coal had a temporary increase from 2021 onwards with a peak in 2022 in which it had a share of 33.3% of the total energy production. In 2021, renewable energy had a weak year and the recovery from the corona pandemic also began. Even though the rise of coal peaked in 2022, renewable energy still had a greater growth in that year.
4. **Outlook 2025:** For 2025, coal has its lowest share in the observed period of only 21.8%. The share of renewable energy is still increasing, but the growth has slowed down.

## Limitations

- The dataset covers only public grid generation (see "Data Source" above) — industrial self-consumption is not included.
- The time range was deliberately limited to 2015–2025 to ensure consistent data quality; earlier events (e.g. Fukushima, 2011) fall outside this window.
- Electricity imports and exports are not part of the data. Changes in total generation (e.g. after the nuclear phase-out) can therefore only be partially explained with this dataset.
- The SMARD API is not officially documented and could change. The API data was validated against a manual SMARD export (identical for 2015–2025), which is kept in `data/raw/` as a fallback.
- Pumped storage is classified under "conventional" energy for simplicity, even though it is technically a storage rather than a generation technology.

## Tech Stack

- Python (pandas, matplotlib, requests)
- SMARD REST API
- Jupyter Notebooks
- Streamlit *(planned)*

## AI Assistance

Parts of the code in this project were developed with [Claude Code](https://claude.com/claude-code), an AI coding assistant. Data selection, research questions, interpretation of results and conclusions are my own. AI-assisted commits are marked with a `Co-Authored-By: Claude` line in the git history.

## Setup

```bash
git clone https://github.com/Yoem29/Energy-Development-Germany.git
cd Energy-Development-Germany
pip install -r requirements.txt
```

To update the data with the newest months published by SMARD (run from the project folder):

```bash
python src/fetch_smard_data.py   # downloads the data into data/raw/
python src/clean_smard_data.py   # creates data/processed/energy_generation_clean.csv
```

## Author

Yoem29 — [GitHub](https://github.com/Yoem29)
