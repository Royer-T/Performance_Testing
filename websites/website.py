import requests


class Website:
    @staticmethod
    def website_up(url):
        """
        Check if a website is up and running.

        :param url: The URL of the website being checked.
        :return: True if the website is up and the response status code is between
        200 and 399 (inclusive), False otherwise
        :rtype: bool
        """
        try:
            response = requests.get(url)
            return 200 <= response.status_code < 400
        except requests.exceptions.RequestException:
            return False
