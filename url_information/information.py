import requests
import re


class Info:
    def __init__(self, url):
        """
        Initializes an instance of the Info class.

        Args:
            url (str): The URL to be stored.
        """
        self.url = url

    def environment(self):
        """
        Determines the environment based on the URL.

        Returns:
            str: The environment name in uppercase ('BETA', 'QCC', 'QCL') if a
                 matching substring is found in the URL, otherwise returns 'PROD'.
        """
        substrings = ['beta', 'qcc', 'qcl']
        for substring in substrings:
            if substring in self.url:
                return substring.upper()

        return "PROD"

    def versioning(self):
        environment_name = self.environment()

        environment_urls = {
            'QCC': 'https://qcc.healthtrioconnect.com/version.txt',
            'QCL': 'https://qcl.healthtrioconnect.com/version.txt',
            'BETA': 'https://beta.healthtrioconnect.com/version.txt',
            'PROD': 'https://healthtrioconnect.com/version.txt'
        }

        version_checker = environment_urls.get(environment_name,
                                               environment_urls['PROD'])

        response = requests.get(version_checker)

        if response.status_code == 201:
            version = self.extract_version(response.text)
            branch = self.extract_branch(response.text)

            return {'version': version, 'branch': branch}
        else:
            return None

    @staticmethod
    def extract_version(version_string):
        """
        Extracts the version number from a given version string.

        Args:
            version_string (str): The version string to extract the version number from.

        Returns:
            str or None: The extracted version number if found, or None if no version number is found.
        """
        pattern = r"(\d+\.\d+\.\d+)"
        match = re.search(pattern, version_string)

        if match:
            version = match.group(1)
            return version
        else:
            return None

    @staticmethod
    def extract_branch(version_string):
        """
        Extracts the branch version from a version string.

        Args:
            version_string (str): The version string to extract the branch version from.

        Returns:
            str or None: The extracted branch version if found in the version string, or None if not found.
        """
        pattern = r"release-(\d+\.\d+)\.\d+-"
        match = re.search(pattern, version_string)

        if match:
            branch = match.group(1)
            return branch
        else:
            return None
