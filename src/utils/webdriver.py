from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


class WebDriver(Chrome):
    def __init__(self, options: Options) -> None:
        super().__init__(options)

    pass


class WebDriverUtils:
    @staticmethod
    def get_options() -> Options:
        options = Options()
        options.add_argument("--headless=new")  # Novo modo headless (mais estável no Chrome 109+)
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        return options
