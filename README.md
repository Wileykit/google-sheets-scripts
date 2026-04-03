# Google Sheets Scripts

A collection of Python scripts for interacting with Google Sheets via the Google API.

## Scripts

### `sheets.py`
Converts data between Google Sheets and pandas DataFrames.

- **`sheet_to_dataframe`** — Reads a Google Sheet worksheet into a pandas DataFrame
- **`dataframe_to_sheet`** — Writes a pandas DataFrame back to a Google Sheet worksheet (creates the target tab if it doesn't exist)

## Setup

### Requirements
```
pip install gspread gspread-dataframe pandas
```

### Google Service Account
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a project and enable the **Google Sheets API** and **Google Drive API**
3. Go to **IAM & Admin > Service Accounts** and create a service account
4. Under the **Keys** tab, create a JSON key and download it
5. Share your Google Sheet with the service account email (e.g. `name@project.iam.gserviceaccount.com`) as an **Editor**

### Usage
Update these values in `sheets.py` before running:
```python
CREDENTIALS_FILE = "/path/to/your/service-account-key.json"
SPREADSHEET_ID   = "your-spreadsheet-id"  # from the sheet URL
```

Then run:
```
python sheets.py
```
