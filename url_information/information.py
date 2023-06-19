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

        headers = {
            # 'Authority': 'healthtrioconnect.com',
            # 'Method': 'GET',
            # 'Path': '/version.txt',
            # 'Scheme': 'https',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            #'Cookie': 'cf_clearance=0PhxHvjl4m73IxR8sv0XhnyqCj3vSqxBRz3kRT.BVuc-1687135342-0-160; UBSID=cb6b12c5-6d53-4d68-8741-55392054d6d7; __cf_bm=1Jie22JuGP7dvf1FIY0ccJu1T5auO.8xx0lHYXrHfoY-1687135346-0-Aa8pEPxaPYB+Kfkk3oeWLOggoMWhtx9DBjfwDuMXDeK7v+2+ixS9ho+dgDuEIxaRzVYElMY/Y4GY0jgJhqzPZKv/JXRHP+y81VH1iQS5GMk9; _cfuvid=zo6HDANep4bkTNGDJjvRFSTB2Z7q2tGiYB2rsc0nwfY-1687135346336-0-604800000',
            'Cookie': 'cf_autotest=3d864a41462695e19d9a90a0b340ca3f6d63c014'
            # 'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            # 'Sec-Ch-Ua-Mobile': '?0',
            # 'Sec-Ch-Ua-Platform': '"Windows"',
            # 'Sec-Fetch-Dest': 'document',
            # 'Sec-Fetch-Mode': 'navigate',
            # 'Sec-Fetch-Site': 'none',
            # 'Sec-Fetch-User': '?1',
            # 'Upgrade-Insecure-Requests': '1',
            ##'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

        response = requests.get(version_checker, headers=headers)

        if response.status_code == 200:
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
