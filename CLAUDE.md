# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Beginner data science portfolio project analyzing Germany's electricity generation 2015–2025 from SMARD (Bundesnetzagentur) monthly data. Three research questions drive the analysis (see README): renewable vs. conventional development, impact of the nuclear phase-out (April 2023), and the coal rise during the 2022 energy crisis. A Streamlit dashboard is planned but not started.

The owner is learning data science — explain changes briefly, prefer plain pandas/matplotlib solutions, and do not rewrite the interpretive markdown text in notebooks unless asked.

## Running

There is no build, lint, or test setup. Dependencies: pandas, matplotlib, jupyter (the README references `requirements.txt`, which does not exist yet).

Notebooks live in `notebooks/` and use relative paths (`../data/...`, `sys.path.append("../src")`), so they must be run with `notebooks/` as the working directory.

## Data pipeline

1. `data/raw/Realisierte_Erzeugung_..._Monat.csv` — unmodified SMARD export. Never edit it.
2. `src/clean_smard_data.py::clean_smard_erzeugung()` turns the raw export into the clean dataframe:
   - `;` separator, German number format (`1.234,56`) → float
   - `"-"` is treated as NaN; only `Kernenergie` has these (months after the 2023 phase-out) and they are filled with 0
   - strips the `Berechnete Auflösungen` suffix from column names
   - adds a `[TWh]` copy of every `[MWh]` column, plus `Jahr` and `Monat` (German month names); drops `Datum bis`
3. `notebooks/EDA.ipynb` calls the cleaning function and **writes** `data/processed/energiedaten_clean.csv`. There is no standalone script for this step, so changes to the cleaning logic need the EDA notebook re-run to update the processed CSV.
4. `notebooks/Analysis.ipynb` reads the processed CSV via `src/load_processed_data.py::load_data()`, which restores `Monat` as an ordered categorical (CSV round-trips lose the ordering, so plots would otherwise sort months alphabetically).

## Conventions

- Column names stay German, as in SMARD (`Braunkohle [MWh]`, `Jahr`, `Monat`). Notebook prose and code comments are in English.
- The `[MWh]` columns are for calculations and the `[TWh]` columns for plots.
- Renewable vs. conventional grouping: renewable = Biomasse, Wasserkraft, Wind Offshore, Wind Onshore, Photovoltaik, Sonstige Erneuerbare; conventional = Kernenergie, Braunkohle, Steinkohle, Erdgas, Pumpspeicher, Sonstige Konventionelle. Pumped storage counting as conventional is a deliberate simplification documented in the README's Limitations section.
- These column lists are currently duplicated in `src/clean_smard_data.py` and both notebooks. Keep them in sync when you edit them.
- Data scope is public-grid net generation only (no industrial self-consumption or closed networks). Keep this in mind when you interpret results.
