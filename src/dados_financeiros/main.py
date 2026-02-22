import sqlite3

import gspread

from dados_financeiros.config.envs import SPREADSHEET_ID

from .utils.logger import logger
from .utils.webdriver import WebDriver, WebDriverUtils
from .workflows.acoes import scrapper_acoes
from .workflows.fiis import scrapper_fiis


def log_query(sql: str) -> None:
    logger.debug(sql)


def main() -> None:
    try:
        gc = gspread.oauth(credentials_filename="credentials.json", authorized_user_filename="token.json")
        options = WebDriverUtils.get_options()
        driver = WebDriver(options=options)

        conn = sqlite3.connect("acoes.db")
        conn.set_trace_callback(log_query)

        with driver, conn:
            scrapper_acoes(gc=gc, conn=conn, driver=driver, spreadsheet_id=SPREADSHEET_ID)
            # scrapper_fiis(gc=gc, conn=conn, driver=driver, spreadsheet_id=SPREADSHEET_ID)

    except Exception as err:
        logger.error(err, exc_info=True)
