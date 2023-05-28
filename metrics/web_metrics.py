import constants
import json
import pycurl
import time
from selenium_navigation.webdriver import ChromeDriver


class WebMetrics:
    def __init__(self, url):
        self.url = url

    def calculate_ttfb(self):
        """
        Calculates Time To First Byte (TTFB) by making an HTTP request to
        the specified URL.

        :parameter: URL where the TTFB is to be calculated (str)
        :return: A JSON string containing the following metrics:
        - 'dns_lookup': Time taken in milliseconds to perform the DNS lookup.
        - 'connect_time': Time taken in milliseconds to establish the
        connection.
        - 'start_transfer_time': Time taken in milliseconds to receive the first
        byte.
        - 'total_time': Total time in milliseconds taken for the entire HTTP
        request.
        :rtype: str (a JSON string)
        """
        # create and instance of 'Curl' from the 'pycurl' module
        curl = pycurl.Curl()

        # specifies the URL to connect to when making an HTTP request
        curl.setopt(pycurl.URL, self.url)

        #  automatically follow HTTP redirects until it reaches the final
        #  destination URL
        curl.setopt(pycurl.FOLLOWLOCATION, 1)

        #  execute the HTTP request
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

        # closes Curl instance and releases any resources associated with it
        curl.close()

        curl_metrics = json.dumps({'dns_lookup': ms_dns_time,
                                   'connect_time': ms_connect_time,
                                   'start_transfer_time': ms_start_transfer_time,
                                   'total_time': ms_total_time})

        return curl_metrics

    def calculate_page_load_time(self):
        """
        Calculates the page load time for a given URL using Chrome WebDriver.

        :return: The page load time in milliseconds
        :rtype: int
        :raise: WebDriverException: If an error occurs while starting the
        Chrome browser or navigating to the URL.
        """
        # need an instance of Chrome (chromedriver)
        # create an object of the class, invokes a parameterized constructor
        driver_instance = ChromeDriver(constants.CHROMEDRIVER)

        #  start the browser/webdriver
        driver = driver_instance.start_chrome()

        # navigate to the URL being evaluated
        driver.get(self.url)

        # wait for the page to load
        while driver.execute_script('return document.readyState') != 'complete':
            time.sleep(0.1)

        # Get the page load time
        navigation_start = driver.execute_script('return window.performance.'
                                                 'timing.navigationStart')
        load_event_end = driver.execute_script('return window.performance.'
                                               'timing.loadEventEnd')
        page_load_time = load_event_end - navigation_start

        # quit the browser
        driver.quit()

        # Return the page load time
        return page_load_time
