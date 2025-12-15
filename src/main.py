import sqlite3
from datetime import datetime
from os import getenv

import gspread
from dotenv import load_dotenv
from googleapiclient.errors import HttpError

from src.scrappers.acoes import scrapper_acoes
from src.utils.webdriver import WebDriver, WebDriverUtils

from .utils.logger import logger

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = getenv("SPREADSHEET_ID")

HOJE = datetime.now().strftime("%Y-%m-%")

def main() -> None:
  if SAMPLE_SPREADSHEET_ID is None:
      raise ValueError("SPREADSHEET_ID environment variable not set")
  try:
    gc = gspread.oauth(credentials_filename="credentials.json", authorized_user_filename="token.json")
    options = WebDriverUtils.get_options()
    driver = WebDriver(options=options)

    conn = sqlite3.connect("acoes.db")
    conn.set_trace_callback(log_query)

    with driver, conn:
      scrapper_acoes(gc=gc, conn=conn, driver=driver, spreadsheet_id=SAMPLE_SPREADSHEET_ID )

  except HttpError as err:
    logger.error(err)


def log_query(sql: str) -> None:
    logger.info(sql)
