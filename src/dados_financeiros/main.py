import sqlite3
from time import sleep

import gspread
from playwright.sync_api import sync_playwright

from dados_financeiros.config.envs import SPREADSHEET_ID

from .utils.logger import logger
from .workflows.acoes import scrapper_acoes
from .workflows.fiis import scrapper_fiis


def log_query(sql: str) -> None:
    logger.debug(sql)


def main() -> None:
    try:
        gc = gspread.oauth(
            credentials_filename="credentials.json",
            authorized_user_filename="token.json",
        )

        conn = sqlite3.connect("acoes.db")
        conn.set_trace_callback(log_query)

        with sync_playwright() as play, conn:
            browser = play.chromium.launch(headless=True)

            page = browser.new_page()

            scrapper_acoes(gc=gc, conn=conn, page=page, spreadsheet_id=SPREADSHEET_ID)
            scrapper_fiis(gc=gc, conn=conn, page=page, spreadsheet_id=SPREADSHEET_ID)

    except Exception as err:
        logger.error(err, exc_info=True)
