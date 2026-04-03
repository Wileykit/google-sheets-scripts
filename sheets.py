import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from google.oauth2.service_account import Credentials

# ── Auth ──────────────────────────────────────────────────────────────────────

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]

def get_client(credentials_path: str) -> gspread.Client:
    """
    Authenticate and return a gspread client.

    Args:
        credentials_path: Path to your service account JSON key file.
    """
    creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    return gspread.authorize(creds)


# ── Google Sheet → pandas ─────────────────────────────────────────────────────

def sheet_to_dataframe(
    client: gspread.Client,
    spreadsheet_id: str,
    sheet_name: str = None,
    evaluate_formulas: bool = True,
    **kwargs,
) -> pd.DataFrame:
    """
    Read a Google Sheet worksheet into a pandas DataFrame.

    Args:
        client:            Authenticated gspread client.
        spreadsheet_id:    The ID from the sheet URL
                           (docs.google.com/spreadsheets/d/<ID>/edit).
        sheet_name:        Worksheet tab name. Defaults to the first sheet.
        evaluate_formulas: If True, returns computed cell values instead of
                           raw formula strings.
        **kwargs:          Extra keyword args forwarded to gspread_dataframe's
                           get_as_dataframe (e.g. usecols, dtype, nrows).

    Returns:
        A pandas DataFrame with the sheet contents.
    """
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = (
        spreadsheet.worksheet(sheet_name)
        if sheet_name
        else spreadsheet.get_worksheet(0)
    )

    df = get_as_dataframe(
        worksheet,
        evaluate_formulas=evaluate_formulas,
        **kwargs,
    )

    # gspread_dataframe pads with NaN columns/rows for empty trailing cells;
    # drop fully-empty rows and columns.
    df = df.dropna(how="all").dropna(axis=1, how="all")
    return df


# ── pandas → Google Sheet ─────────────────────────────────────────────────────

def dataframe_to_sheet(
    client: gspread.Client,
    df: pd.DataFrame,
    spreadsheet_id: str,
    sheet_name: str = None,
    clear_first: bool = True,
    include_index: bool = False,
    resize: bool = True,
    **kwargs,
) -> None:
    """
    Write a pandas DataFrame to a Google Sheet worksheet.

    Args:
        client:          Authenticated gspread client.
        df:              The DataFrame to upload.
        spreadsheet_id:  The ID from the sheet URL.
        sheet_name:      Worksheet tab name. Defaults to the first sheet.
        clear_first:     Wipe the worksheet before writing (prevents stale data).
        include_index:   Whether to write the DataFrame index as a column.
        resize:          Resize the worksheet to fit the DataFrame exactly.
        **kwargs:        Extra keyword args forwarded to set_with_dataframe.
    """
    spreadsheet = client.open_by_key(spreadsheet_id)

    if sheet_name:
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(sheet_name, rows=1000, cols=26)
    else:
        worksheet = spreadsheet.get_worksheet(0)

    if clear_first:
        worksheet.clear()

    set_with_dataframe(
        worksheet,
        df,
        include_index=include_index,
        resize=resize,
        **kwargs,
    )
    print(f"Wrote {len(df)} rows x {len(df.columns)} cols to '{worksheet.title}'")


# ── Example usage ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import os
    CREDENTIALS_FILE = os.environ.get("GOOGLE_CREDENTIALS_FILE", "/Users/kpw3/Downloads/coding-club-project-465518-b8b1326a460d.json")
    SPREADSHEET_ID   = os.environ.get("SPREADSHEET_ID", "1Wtt6fZwTsxiiz54dtGiuNmqiCF-d0R3W0kbvPgU04b4")

    client = get_client(CREDENTIALS_FILE)

    # Read Sheet1 → DataFrame
    df = sheet_to_dataframe(client, SPREADSHEET_ID, sheet_name="Sheet1")
    print(df.head())

    # Example: double a numeric column — replace "some_existing_col" with your actual column name
    # df["new_col"] = df["some_existing_col"] * 2

    # Write DataFrame → Output tab (creates it if it doesn't exist)
    dataframe_to_sheet(client, df, SPREADSHEET_ID, sheet_name="Output")
