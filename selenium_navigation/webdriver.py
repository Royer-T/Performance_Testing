from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class ChromeDriver:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = None

    def start_chrome(self):
        """
        Starts a Chrome browser session and returns the WebDriver instance.

        :parameter: Path to the ChromeDriver executable.
        :return: Chrome WebDriver instance
        :rtype: class (selenium.webdriver.chrome.webdriver.WebDriver)
        :raise: WebDriverException: If an error occurs while starting the
        Chrome browser.
        """
        # set Chrome options
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')

        # set the chromedriver
        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        return driver

    def stop(self):
        self.driver.quit()

    def navigatio(self, url):
        self.driver.get(url)

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def close(self):
        self.driver.close()
