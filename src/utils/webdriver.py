


from selenium.webdriver import Chrome, ChromeOptions


class WebDriver(Chrome):
    pass



class WebDriverUtils(ChromeOptions):
    @staticmethod
    def get_options():
        options = ChromeOptions()
        options.add_argument('--headless')

        return options