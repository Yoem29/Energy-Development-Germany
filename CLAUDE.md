# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Beginner data science portfolio project analyzing Germany's electricity generation 2015–2025 from SMARD (Bundesnetzagentur) monthly data. Three research questions drive the analysis (see README): renewable vs. conventional development, impact of the nuclear phase-out (April 2023), and the coal rise during the 2022 energy crisis. Data is fetched from the SMARD API. A Streamlit dashboard is planned but not started.

The owner is learning data science — explain changes briefly, prefer plain pandas/matplotlib solutions, and do not rewrite the interpretive markdown text in notebooks unless asked.

The owner works mainly in VS Code: whenever giving git/GitHub instructions or terminal commands, also describe the VS Code way (Source Control panel, Command Palette, status bar branch picker, GitHub Pull Requests extension).

## Running

There is no build, lint, or test setup. Install dependencies with `pip install -r requirements.txt`.

Update the data (run from the repo root; the scripts resolve paths relative to their own location):

```bash
python src/fetch_smard_data.py   # SMARD API -> data/raw/smard_generation_monthly.csv
python src/clean_smard_data.py   # -> data/processed/energy_generation_clean.csv (2015-2025 only)
```

Notebooks live in `notebooks/` and use relative paths (`../data/...`, `sys.path.append("../src")`), so they must be run with `notebooks/` as the working directory. Modules in `src/` import each other by plain module name (`from config import ...`), which works both from the notebooks and when running the scripts directly.

## Data pipeline

1. `src/fetch_smard_data.py` downloads the monthly series of all 12 energy sources from the public SMARD API (`https://www.smard.de/app/chart_data/{filter}/DE/...`). The API returns yearly blocks of `[timestamp_ms, MWh]` pairs; timestamps are converted to Europe/Berlin so each value starts on the 1st of the month. Unpublished months and nuclear after 2023 come back as NaN.
2. `src/clean_smard_data.py::clean_smard_api()` fills nuclear NaN with 0, drops unpublished months and adds the derived columns. Running the module as a script writes the processed CSV limited to `START_YEAR`–`END_YEAR`.
3. `src/clean_smard_data.py::clean_smard_export()` cleans the manual csv export (`data/raw/Realisierte_Erzeugung_..._Monat.csv`, kept unmodified as reference): `;` separator, German number format, `"-"` as NaN, strips `Berechnete Auflösungen`, translates German column names via `EXPORT_TRANSLATION` (unknown columns print a warning). Both cleaners share `add_derived_columns()` (`[TWh]` copies, `Year`, `Month`) and produce identical output.
4. `notebooks/EDA.ipynb` walks through the manual export and, in section 3, validates the API data against it (difference is 0 for 2015–2025).
5. `notebooks/Analysis.ipynb` reads the processed CSV via `src/load_processed_data.py::load_data()`, which restores `Month` as an ordered categorical (CSV round-trips lose the ordering, so plots would otherwise sort months alphabetically).

## Conventions

- Column names are English (`Lignite [MWh]`, `Year`, `Month`). Only the raw-data exploration cells in the EDA notebook show the original German SMARD names. Notebook prose and code comments are in English.
- `src/config.py` is the single source of truth for energy sources, SMARD filter IDs, column lists (`ENERGY_COLUMNS`, `RENEWABLE_COLUMNS`, `CONVENTIONAL_COLUMNS` and `_TWH` variants), the German→English translation and the observation period. Import from there instead of redefining lists.
- The `[MWh]` columns are for calculations and the `[TWh]` columns for plots.
- Pumped storage counting as conventional is a deliberate simplification documented in the README's Limitations section.
- Data scope is public-grid net generation only (no industrial self-consumption, closed networks or imports). Keep this in mind when you interpret results.
