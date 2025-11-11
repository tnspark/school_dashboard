# TN Spark Analytical Dashboard

A modern, sleek Streamlit app for analyzing TN SPARK EMIS data with interactive charts, filters, and CSV upload support.

## Features
- Tabbed layout: Overview, Schools, Chapters, Syllabus, More
- KPI cards and improved Plotly visualizations
- Sidebar filters by district and class
- Upload daily CSV reports (replace or append) and auto-refresh
- Data quality summary and CSV export

## Local Run
1. Install Python 3.11 (recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run dashboard_streamlit.py
   ```

## Deploy to Streamlit Community Cloud
1. Push this project to GitHub (see steps below).
2. Go to https://share.streamlit.io/ (or https://streamlit.io/cloud) and create a new app.
3. Select your GitHub repo, branch `main`, and set the app file to `dashboard_streamlit.py`.
4. Streamlit will install from `requirements.txt` and build your app.

## Publish to GitHub
From the project root:
```bash
git init
git add .
git commit -m "Initial commit: TN Spark Streamlit dashboard"
# Create a new repo on GitHub, then set the remote URL:
# Replace <username> and <repo> accordingly
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

## Notes
- Default data file: `TN SPARK Overall reportReport (8).csv` (place in repo root).
- You can upload CSVs from the sidebar to dynamically update the dashboard.
- App theme is configured via `.streamlit/config.toml`.