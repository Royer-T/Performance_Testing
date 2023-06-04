from io import BytesIO

import pycurl
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WebMetrics:
    """
    Initializes a WebMetrics object with the specified URL.

    :param url: The URL to measure the web metrics for.
    :type url: str
    """
    def __init__(self, url):
        self.url = url
        self.curl = pycurl.Curl()

    def __del__(self):
        """
        Destructor that closes the pycurl.Curl object when the WebMetrics
        object is destroyed.
        """
        self.curl.close()

    def calculate_ttfb(self):
        """
        Calculates the Time To First Byte (TTFB) for the specified URL.

        :return: A dictionary containing the following TTFB metrics in milliseconds:
                 - 'dns_lookup': Time taken for DNS lookup
                 - 'connect_time': Time taken to establish the connection
                 - 'start_transfer_time': Time taken to receive the first byte
                 - 'total_time': Total time taken for the entire HTTP request
        :rtype: dict
        """
        with BytesIO() as buffer:
            self.curl.setopt(pycurl.URL, self.url)
            self.curl.setopt(self.curl.WRITEFUNCTION, buffer.write)
            self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
            self.curl.perform()

            dns_time = self.curl.getinfo(pycurl.NAMELOOKUP_TIME)
            connect_time = self.curl.getinfo(pycurl.CONNECT_TIME)
            start_transfer_time = self.curl.getinfo(pycurl.STARTTRANSFER_TIME)
            total_time = self.curl.getinfo(pycurl.TOTAL_TIME)

            curl_metrics = {
                'dns_lookup': round(dns_time * 1000),
                'connect_time': round(connect_time * 1000),
                'start_transfer_time': round(start_transfer_time * 1000),
                'total_time': round(total_time * 1000)
            }

            return curl_metrics

    def calculate_page_load(self, driver):
        """
        Calculates the page load time for the specified URL.

        :param driver: ChromeDriver instance to use for navigating to the URL.
        :type driver: ChromeDriver
        :return: The page load time in milliseconds.
        :rtype: int
        """
        driver.get(self.url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//body')))
        navigation_start = driver.execute_script('return window.performance.timing.navigationStart')
        load_event_end = driver.execute_script('return window.performance.timing.loadEventEnd')
        page_load_time = load_event_end - navigation_start

        driver.execute_cdp_cmd('Network.clearBrowserCache', {})

        return page_load_time

    def calculate_ttfp(self, driver):
        """
        Calculates the Time to First Paint (TTFP) for a given URL using the
        provided ChromeDriver instance.

        :param driver: ChromeDriver instance to use for navigating to the URL.
        :type driver: ChromeDriver
        :return: The TTFP value rounded to the nearest integer.
        :rtype: int
        """
        driver.get(self.url)
        ttfp_time_float = driver.execute_script("return window.performance.getEntriesByType('paint')[0].startTime")
        ttfp_int = round(ttfp_time_float)

        driver.execute_cdp_cmd('Network.clearBrowserCache', {})

        return ttfp_int
