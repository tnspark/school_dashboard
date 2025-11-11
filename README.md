# TN SPARK Analytical Dashboard

Simple, well-documented Streamlit application for exploring TN SPARK EMIS data. It includes clear filters, metrics, tables, and charts with a clean UI. The code is thoroughly commented for easy maintenance.

## Features
- District and Class filters with sensible defaults
- Key metrics: Schools, Teachers, Classes, Average Completion
- Tabs for Overview (data quality), Schools, Chapters, and Syllabus
- CSV upload support (replace or append to base dataset)
- Optional chart PNG exports when `kaleido` is installed

## Project Structure
- `dashboard_streamlit.py` — Full-featured, commented Streamlit app
- `requirements.txt` — Python dependencies for local run and Cloud
- `run_dashboard.bat` — Windows helper script to create venv and run app
- `TN SPARK Overall reportReport (8).csv` — Default dataset used by the app
- `.gitignore` — Git ignore rules

## Prerequisites
- Python 3.10+ recommended
- Internet access to install dependencies

## Quickstart (Windows)
1. Double-click `run_dashboard.bat` (recommended), or run in a terminal within the repo folder:
   - It creates a virtual environment in `%LocalAppData%\tnspark-venv`
   - Installs dependencies from `requirements.txt`
   - Launches `dashboard_streamlit.py` on `http://localhost:8502/`

2. Manual alternative (PowerShell):
   - `py -m venv "$env:LocalAppData\tnspark-venv"`
   - `& "$env:LocalAppData\tnspark-venv\Scripts\pip.exe" install -r requirements.txt`
   - `& "$env:LocalAppData\tnspark-venv\Scripts\python.exe" -m streamlit run dashboard_streamlit.py`

## Data
- The app loads `TN SPARK Overall reportReport (8).csv` by default if present.
- You can upload one or more CSVs via the sidebar and choose to replace or append.
- To use a different default file, either rename your CSV to match the expected name or update the path in `load_data()` inside `dashboard_streamlit.py`.

## Deployment (Streamlit Cloud)
1. Push this repo to GitHub (already done).
2. In Streamlit Cloud:
   - App file: `dashboard_streamlit.py`
   - Python version: 3.10+
   - Requirements: use `requirements.txt`
3. If your dataset is large or private:
   - Remove the local CSV from the repo and rely on uploads, or
   - Use a secure data source (S3, database, etc.) and adapt `load_data()`.

## Troubleshooting
- CSV not found: Ensure `TN SPARK Overall reportReport (8).csv` is in the repo root or upload via the sidebar.
- Encoding issues: The uploader tries UTF‑8, then Latin‑1.
- Port already in use: Close other Streamlit apps or change port via `--server.port`.
- OneDrive path issues: `run_dashboard.bat` creates venv in `%LocalAppData%` to avoid file locks.

## Notes
- Advanced features (AgGrid tables, click‑to‑filter events, PNG exports) are enabled by the full dependency set in `requirements.txt`.
- If you don’t need exports or advanced tables, you can remove `kaleido`, `reportlab`, `openpyxl`, `streamlit-aggrid`, and `streamlit-plotly-events` from `requirements.txt`.
