import sqlite3
from os import getenv
import threading

import gspread
from dotenv import load_dotenv
from googleapiclient.errors import HttpError

from .utils.logger import logger
from .utils.webdriver import WebDriver, WebDriverUtils
from .workflows.acoes import scrapper_acoes
from .workflows.fiis import scrapper_fiis

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = getenv("SPREADSHEET_ID")


def main() -> None:
    if SPREADSHEET_ID is None:
        raise ValueError("SPREADSHEET_ID environment variable not set")
    try:
        gc = gspread.oauth(credentials_filename="credentials.json", authorized_user_filename="token.json")
        options = WebDriverUtils.get_options()
        driver = WebDriver(options=options)

        conn = sqlite3.connect("acoes.db")
        conn.set_trace_callback(log_query)

        with driver, conn:
            scrapper_acoes(gc=gc, conn=conn, driver=driver, spreadsheet_id=SPREADSHEET_ID)
            scrapper_fiis(gc=gc, conn=conn, driver=driver, spreadsheet_id=SPREADSHEET_ID)

    except HttpError as err:
        logger.error(err)


def log_query(sql: str) -> None:
    logger.debug(sql)
