# Energy Development Germany 2015–2025

> 🚧 This project is currently in progress. This README will be updated as the project develops.

Showcase project analyzing the development of Germany's electricity production between 2015 and 2025, based on official data from SMARD (Bundesnetzagentur).

## Current Status

- ✅ Data cleaning
- ✅ Exploratory Data Analysis (EDA)
- 🔄 Analysis (in progress)
- ⬜ Dashboard (planned, via Streamlit)

## Motivation

The transition toward renewable energy is a central topic in Germany's energy policy. This project examines how the country's electricity mix has actually developed over the past decade, and what role major events — such as the coal phase-out law, the 2022 energy crisis, and the final nuclear phase-out — played in that development.

## Research Questions

1. How has renewable energy production developed compared to conventional energy production?
2. What impact did the shutdown of nuclear energy (April 2023) have on other energy producers?
3. How did the 2022 energy crisis influence the temporary rise of coal-based energy production?

## Data Source

- **Provider:** [SMARD](https://www.smard.de) (Bundesnetzagentur / German Federal Network Agency)
- **Metric:** Realized (net) electricity generation, i.e. electricity actually fed into the public grid
- **Time range:** 2015–2025
- **Resolution:** Monthly
- **License:** CC BY 4.0

**Note on data scope:** The data reflects generation from the public electricity grid only. It does not include self-generated electricity consumed directly by industrial facilities, nor generation within closed distribution networks (e.g. Deutsche Bahn). It also excludes grid losses and the self-consumption of power plants. This is the standard scope used across most German energy statistics (SMARD, Destatis, Fraunhofer ISE) and remains consistent across the entire observation period.

## Project Structure

```
├── data/
│   ├── raw/            # Original SMARD export (unmodified)
│   └── processed/       # Cleaned data, ready for analysis
├── notebooks/
│   ├── EDA.ipynb         # Data cleaning walkthrough and first insights
│   └── Analysis.ipynb    # In-depth analysis of the research questions
├── src/
│   ├── clean_smard_data.py     # Cleaning logic for SMARD raw exports
│   └── load_processed_data.py  # Helper to load processed data with correct month ordering
└── .gitignore
```

## Methodology

1. **Cleaning** – Raw SMARD export (German number format, missing-value placeholders, inconsistent column names) is transformed into a consistent, analysis-ready dataset.
2. **EDA** – Initial exploration of the cleaned data: data types, value ranges, and first visible patterns (e.g. the nuclear phase-out showing up as a structural break).
3. **Analysis** – Each research question is examined individually, combining yearly trends with monthly detail where relevant.
4. **Dashboard** *(planned)* – An interactive Streamlit dashboard to explore the data and findings.

## Key Findings

*To be added once the analysis is complete.*

## Limitations

- The dataset covers only public grid generation (see "Data Source" above) — industrial self-consumption is not included.
- The time range was deliberately limited to 2015–2025 to ensure consistent data quality; earlier events (e.g. Fukushima, 2011) fall outside this window.
- Pumped storage is classified under "conventional" energy for simplicity, even though it is technically a storage rather than a generation technology.

## Tech Stack

- Python (pandas, matplotlib)
- Jupyter Notebooks
- Streamlit *(planned)*

## Setup

```bash
git clone https://github.com/Yoem29/Energy-Development-Germany.git
cd Energy-Development-Germany
pip install -r requirements.txt
```

## Author

Yoem29 — [GitHub](https://github.com/Yoem29)
