# Dev Log

## 2026-04-03 — Initial Setup

### Goal
Set up a Google Service Account and write a Python script to read/write Google Sheets data using pandas.

### Steps Taken

1. **Created a Google Cloud project** ("Coding Club Project") at console.cloud.google.com
2. **Created a Service Account** under IAM & Admin > Service Accounts
3. **Downloaded the JSON key** from the Keys tab of the service account
4. **Installed dependencies**:
   ```
   pip install gspread gspread-dataframe pandas
   ```
5. **Wrote `sheets.py`** — functions to convert between Google Sheets and pandas DataFrames
6. **Fixed permissions** — shared the Google Sheet with the service account email as Editor
7. **Confirmed working** — script successfully reads Sheet1 into a DataFrame and writes to an Output tab

### Issues & Fixes

| Issue | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'gspread_dataframe'` | Ran `pip install gspread gspread-dataframe` |
| `APIError: [403]: The caller does not have permission` | Shared the Google Sheet with the service account email as Editor |
| Wrong Spreadsheet ID in code | Corrected to ID extracted from sheet URL |
| Output tab didn't exist | Added auto-create logic for missing worksheets |
