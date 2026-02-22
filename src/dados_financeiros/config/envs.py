from os import getenv

from dotenv import load_dotenv

load_dotenv()

# The ID and range of a sample spreadsheet.
_SPREADSHEET_ID = getenv("SPREADSHEET_ID")
if _SPREADSHEET_ID is None:
    raise ValueError("SPREADSHEET_ID environment variable not set")

SPREADSHEET_ID = _SPREADSHEET_ID
