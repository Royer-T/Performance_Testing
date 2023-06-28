import pycurl
from io import BytesIO


class CurlMetrics:
    """
    A class for calculating various metrics related to Curl requests.
    """

    def __init__(self, url):
        """
        Initialize CurlMetrics object with the specified URL.

        Args:
        url (str): The URL to perform Curl requests.
        """
        self.url = url
        self.curl = pycurl.Curl()

    def __del__(self):
        """
        Clean up the Curl object when the CurlMetrics object is destroyed.
        """
        self.curl.close()

    def calculate_ttfb(self):
        """
        Perform a Curl request and calculate the time to first byte (TTFB).

        Returns:
        dict: A dictionary containing the following metrics:
            - dns_lookup (int): Time taken for DNS lookup in milliseconds.
            - connect_time (int): Time taken to establish a connection in
            milliseconds.
            - start_transfer_time (int): Time when the first byte is received
            in milliseconds.
            - total_time (int): Total time taken for the request in
            milliseconds.
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

