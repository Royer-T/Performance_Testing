import logging
import re
import requests

#  set the logging behaviour
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s '
                                                '- %(name)s:%(message)s')
logger = logging.getLogger(__name__)

ENVIRONMENT_URLS = {
    'QCC': 'https://qcc.healthtrioconnect.com/version.txt',
    'QCL': 'https://qcl.healthtrioconnect.com/version.txt',
    'BETA': 'https://beta.healthtrioconnect.com/version.txt',
    'PROD': 'https://healthtrioconnect.com/version.txt'
}


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
                environment = substring.upper()
                logger.info(f'Environment: {environment}')
                return environment

        logger.info('Environment: PROD')
        return 'PROD'

    def versioning(self):
        """
        Retrieves the application version and branch based on the environment.

        Returns:
            dict or None: A dictionary containing the version and branch if
            successfully retrieved, or None if the version and branch could not
            be determined.
        """
        environment_name = self.environment()
        version_checker = ENVIRONMENT_URLS.get(environment_name,
                                               ENVIRONMENT_URLS['PROD'])

        try:
            response = requests.get(version_checker)
            response.raise_for_status()
        except (requests.RequestException, ValueError):
            logger.warning('Could not determine application version')
            logger.warning('Could not determine application branch')
            return None

        version = self.extract_version(response.text)
        branch = self.extract_branch(response.text)

        return {'version': version, 'branch': branch}

    @staticmethod
    def extract_version(version_string):
        """
        Extracts the version number from a given version string.

        Args:
            version_string (str): The version string to extract the version
            number from.

        Returns:
            str or None: The extracted version number if found, or None if no
            version number is found.
        """
        pattern = r"(\d+\.\d+\.\d+)"
        match = re.search(pattern, version_string)

        if match:
            version = match.group(1)
            logger.info(f'Version: {version}')
            return version

        logger.warning('Could not determine application version')
        return None

    @staticmethod
    def extract_branch(version_string):
        """
        Extracts the branch version from a version string.

        Args:
            version_string (str): The version string to extract the branch
            version from.

        Returns:
            str or None: The extracted branch version if found in the version
            string, or None if not found.
        """
        pattern = r"release-(\d+\.\d+)\.\d+-"
        match = re.search(pattern, version_string)

        if match:
            branch = match.group(1)
            logger.info(f'Branch: {branch}')
            return branch

        logger.warning('Could not determine application branch')
        return None
