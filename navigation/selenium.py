from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class AutoNavigation:
    def __init__(self):
        pass

    @staticmethod
    def create_chrome_driver(chromedriver_path):
        """
        Create a Chrome WebDriver instance.

        :param chromedriver_path: The path to the ChromeDriver executable (str)
        :return: A Chrome WebDriver instance.
        :rtype: selenium.webdriver.Chrome
        :raise: WebDriverException: If the ChromeDriver fails to start.
        """
        # set Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-popup-blocking')

        # set up chromedriver
        driver = webdriver.Chrome(chromedriver_path, options=chrome_options)

        return driver
