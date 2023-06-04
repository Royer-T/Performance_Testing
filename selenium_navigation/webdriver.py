from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ChromeDriver:
    @staticmethod
    def start_chrome(chrome_path, driver_path):
        """
        Starts a Chrome browser session using the provided paths to Chrome
        executable and ChromeDriver, and returns the WebDriver instance.

        :param: Path to the Chrome executable (chrome.exe).
        :param: Path to the ChromeDriver executable (chromedriver.exe).
        :return: Chrome WebDriver instance.
        :rtype: selenium.webdriver.chrome.webdriver.WebDriver
        :raise: selenium.common.exceptions.WebDriverException: If an error
        occurs while starting the Chrome browser.
        """
        # set Chrome options
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument("--disable-cache")
        options.add_argument("--disk-cache-size=0")
        options.binary_location = chrome_path

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(executable_path=driver_path,
                                  options=options, service=service)

        return driver
