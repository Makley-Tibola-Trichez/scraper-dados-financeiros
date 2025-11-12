from datetime import datetime
import sqlite3

from os import getenv
from googleapiclient.errors import HttpError
import gspread
from dotenv import load_dotenv

from src.utils.webdriver import WebDriver, WebDriverUtils
from src.scrappers.acoes import scrapperAcoes
load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = getenv("SPREADSHEET_ID")

HOJE = datetime.now().strftime('%Y-%m-%d')

def main():
  if SAMPLE_SPREADSHEET_ID is None:
      raise ValueError("SPREADSHEET_ID environment variable not set")
  try:
    gc = gspread.oauth(credentials_filename='credentials.json', authorized_user_filename='token.json')

    conn = sqlite3.connect('acoes.db')

    options = WebDriverUtils()
    driver = WebDriver(options=options)

    scrapperAcoes(gc=gc, conn=conn, driver=driver, SAMPLE_SPREADSHEET_ID=SAMPLE_SPREADSHEET_ID )
        
    conn.close()
  except HttpError as err:
    print(err)
  

