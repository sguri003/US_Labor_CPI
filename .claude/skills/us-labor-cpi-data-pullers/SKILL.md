---
name: us-labor-cpi-data-pullers
description: Use when adding a new economic-data source (BLS, BEA, EIA, or similar government API) to the US_Labor_CPI project, or when modifying an existing puller class (CPI_Puller, Power_Delivery, US_Labor_Force, Lumber, EIA_Electricity) or its chart output
---

# US_Labor_CPI data pullers

## Overview
GDS Data Solutions project pulling US economic/labor data (BLS, BEA, EIA) into CSVs for analysis. Location: `US_Labor_CPI/US_Labor_CPI/`. Open source: github.com/sguri003/Labor_Stats_Dev.

## Folder layout (as of 2026-08-09 reorg)
- `scripts/` — all Python code, including a shared `paths.py` (`PROJECT_ROOT`, `DATA_DIR`, `SECRETS_DIR`, resolved via `Path(__file__)` so it works regardless of invocation cwd). Every script imports what it needs from `paths` rather than using bare filenames.
- `data_exports/` — all CSV/output data (pull results, generated frames, charts). Anything a puller writes goes here via `DATA_DIR`.
- `secrets/` — `API_KEY.csv` only. Gitignored (`secrets/` as a whole, per [[feedback_gitignore_secrets_proactively]]). Read via `SECRETS_DIR`.
- Loose reference files (`states.json`, `new_states.json`, `state_format.json`) stay at the project root — not exports, not secrets — referenced via `PROJECT_ROOT` from `dict_qa.py`.

## Puller class pattern
One class per data source, one file per class:
- Constructor: `(reg_key, out_file_nm, series_id/params, start_year, end_year)` — kicks off the pull and write in `__init__`.
- `get_*` method: fires the HTTP request. **Always check `status_code` before parsing the body** — BLS/EIA return HTML error/maintenance pages on non-200, and `json.loads()` on that raises a confusing `JSONDecodeError` instead of a clear cause. Pattern:
  ```python
  if resp.status_code != 200:
      raise RuntimeError(f"<SOURCE> API returned {resp.status_code}: {resp.text[:200]}")
  ```
- `*_to_csv`/`write_csv` method: deletes any existing output file first (prints whether it existed), writes CSV with `csv.QUOTE_ALL`.

## API keys
All keys live in one `secrets/API_KEY.csv`, one column per source (`BLS_API`, `BAE_KEY`, `EIA_KEY` — names as the user set them, don't "fix" the BEA typo). Read with `pd.read_csv(SECRETS_DIR / 'API_KEY.csv')['<COLUMN>'][0]`.

## Source-specific request shapes
- **BLS** (`api.bls.gov/publicAPI/v2/timeseries/data/`): single POST endpoint for all series, `seriesid` is a list, JSON body via `json.dumps(...)`, param key is `registrationkey`.
- **EIA** (`api.eia.gov/v2/...`): GET per route (e.g. `electricity/retail-sales/data/`, `electricity/electric-power-operational-data/data/`), different facets per route, param key is `api_key`. Monthly frequency needs `start`/`end` as `YYYY-MM` (annual just needs the year). Verify a new route live with a throwaway request before wiring it into a class — EIA route/facet names aren't uniform across datasets.
- **BEA**: not yet built (planned: NIPA Table T20600 for personal income + personal saving rate).

## Charting convention
Each puller's class can own a `plot_trends`-style method that reads its own output CSV back and charts it (see `EIA_Electricity.plot_trends`). Follow the `dataviz` skill's procedure:
- Metrics on incompatible scales (e.g. price in cents vs. usage in million kWh) → **small multiples** (stacked subplots sharing the x-axis), never dual y-axes.
- Use the reference categorical palette in fixed order: slot 1 blue `#2a78d6`, slot 2 orange `#eb6834`, slot 3 aqua `#1baf7a` (first three slots are pre-validated all-pairs CVD-safe — no need to re-run the validator for this exact triple).
- Single series per panel needs no legend — the panel title names it.
- 2px lines, hairline gridlines (`#e1e0d9`), muted axis ink (`#898781`/`#52514e`), light surface `#fcfcfb`.
- Save with `fig.savefig(...)` then `plt.show()` so it works both headless (verification) and interactively (user's normal run).

## Common mistakes
- Forgetting the status-code check → cryptic `JSONDecodeError` instead of a clear API-outage message.
- Plotting differently-scaled series on one axis instead of small multiples.
- Assuming an EIA route's facet names without testing live — they differ per dataset.
