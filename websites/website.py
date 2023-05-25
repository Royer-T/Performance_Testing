import requests


class Website:
    def __init__(self, url):
        self.url = url

    def website_up(self):
        """
        Check if a website is up and running.

        :parameter: URL being checked
        :return: if the website is up and the response status code is between
        200 and 399 (inclusive)
        :rtype: bool
        """
        try:
            response = requests.get(self.url)

            if 200 <= response.status_code < 400:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False
