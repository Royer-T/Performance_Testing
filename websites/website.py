import requests


class Website:
    def __init__(self, url):
        """
        Initialize a Website object with the provided URL.

        :param url: The URL of the website being checked.
        """
        self.url = url

    def website_up(self):
        """
        Check if a website is up and running.

        :parameter: URL being checked
        :return: True if the website is up and the response status code is between
        200 and 399 (inclusive), False otherwise
        :rtype: bool
        """
        try:
            response = requests.get(self.url)
            return 200 <= response.status_code < 400
        except requests.exceptions.RequestException:
            return False

