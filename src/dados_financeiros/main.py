import sqlite3

import gspread
from google.auth.exceptions import RefreshError
from playwright.sync_api import sync_playwright

from dados_financeiros.config.config import Config
from dados_financeiros.config.envs import SPREADSHEET_ID

from .utils.logger import logger
from .workflows.acoes import scrapper_acoes
from .workflows.fiis import scrapper_fiis


def main() -> None:
    try:
        gc = gspread.oauth(
            credentials_filename="credentials.json",
            authorized_user_filename="token.json",
        )
    except RefreshError as err:
        logger.exception(err)
        logger.error(
            "O refresh_token salvo em token.json não é mais válido (revogado ou expirado). "
            "Apague o arquivo token.json e rode a aplicação novamente para reautorizar via OAuth."
        )
        return

    try:
        conn = sqlite3.connect(Config.db_path)
        conn.set_trace_callback(logger.debug)

        with sync_playwright() as play, conn:
            browser = play.chromium.launch(headless=True)
            page = browser.new_page()

            scrapper_acoes(gc=gc, spreadsheet_id=SPREADSHEET_ID, page=page, conn=conn)
            scrapper_fiis(gc=gc, spreadsheet_id=SPREADSHEET_ID, page=page, conn=conn)
    except (gspread.exceptions.APIError, RefreshError) as err:
        logger.exception(err)
        logger.error(
            "Falha de autenticação/autorização com a API do Google Sheets durante o scraping. "
            "Se o erro persistir, apague token.json e reautorize."
        )
    except Exception as err:
        logger.exception(err)
