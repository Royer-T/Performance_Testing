import constants
import pycurl
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_navigation.webdriver import ChromeDriver


class WebMetrics:
    def __init__(self, url):
        """
        Initializes a WebMetrics object with the specified URL.

        :param: url (str) The URL to measure the web metrics for.
        """
        self.url = url

    def calculate_ttfb(self):
        """
        Calculates the Time To First Byte (TTFB) for the specified URL.

        :param: The URL to measure the web metrics for
        :return: A dictionary containing the following TTFB metrics in
                milliseconds:
                - 'dns_lookup': Time taken for DNS lookup
                - 'connect_time': Time taken to establish the connection
                - 'start_transfer_time': Time taken to receive the first byte
                - 'total_time': Total time taken for the entire HTTP request
        :rtype:  dict
        """
        curl = pycurl.Curl()
        try:
            curl.setopt(pycurl.URL, self.url)
            buffer = BytesIO()
            curl.setopt(curl.WRITEFUNCTION, buffer.write)
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.perform()

            # gather some information (we are going to want time in ms)
            # 1. time taken in milliseconds to perform the DNS lookup
            dns_time = curl.getinfo(pycurl.NAMELOOKUP_TIME)
            ms_dns_time = round((dns_time * 1000), 0)

            # 2. time it took in milliseconds to establish the connection
            connect_time = curl.getinfo(pycurl.CONNECT_TIME)
            ms_connect_time = round((connect_time * 1000), 0)

            # 3. time it took in milliseconds to receive the first byte (TTFB)
            start_transfer_time = curl.getinfo(pycurl.STARTTRANSFER_TIME)
            ms_start_transfer_time = round((start_transfer_time * 1000), 0)

            # 4. total time in milliseconds taken for the entire HTTP request,
            # from the time Curl initiated the request until the entire response
            # was received.
            total_time = curl.getinfo(pycurl.TOTAL_TIME)
            ms_total_time = round((total_time * 1000), 0)

            curl_metrics = {
                'dns_lookup': ms_dns_time,
                'connect_time': ms_connect_time,
                'start_transfer_time': ms_start_transfer_time,
                'total_time': ms_total_time
            }

            return curl_metrics
        finally:
            curl.close()

    def calculate_page_load_time(self):
        """
        Calculates the page load time for the specified URL.

        :param: The URL to measure the web metrics for
        :return: The page load time in milliseconds.
        :rtype: int
        """
        #  start the browser/webdriver
        driver = ChromeDriver.start_chrome(constants.CHROME_EXE,
                                           constants.CHROMEDRIVER)

        # navigate to the URL being evaluated
        driver.get(self.url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//body')))

        navigation_start = driver.execute_script('return window.performance.timing.navigationStart')
        load_event_end = driver.execute_script('return window.performance.timing.loadEventEnd')
        page_load_time = load_event_end - navigation_start

        driver.quit()

        return page_load_time
