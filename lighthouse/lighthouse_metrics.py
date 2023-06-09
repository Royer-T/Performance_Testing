import json
import logging
import os
import subprocess
from dotenv import load_dotenv
from pathlib import Path

#  constants (includes from .env)
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)


class LighthouseRunner:
    """
    A class for running Lighthouse audits and saving the JSON output to files.
    """

    def __init__(self, output_directory):
        """
        Initialize the LighthouseRunner instance.

        Args:
            output_directory (str): The directory where the JSON output files
            will be saved.
        """
        self.output_directory = output_directory

    def run_lighthouse(self, url, filename):
        """
        Run the Lighthouse audit and save the JSON output to a file.

        Args:
            url (str): The URL to run the Lighthouse audit on.
            filename (str): The desired name of the output file (without
            extension).

        Returns:
            bool: True if successful, False if an error was encountered.
        """
        output_path = os.path.join(self.output_directory, f"{filename}.json")

        command = [
            os.environ.get('LIGHTHOUSE_CMD', 'lighthouse'),
            url,
            "--output=json",
            "--output-path=" + output_path,
            "--no-enable-error-reporting",
            "--no-update-notifier",
            "--chrome-flags=\"--headless\"",
            "--quiet",
            "--preset",
            "desktop"
        ]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            logging.error(f'Failed to run Lighthouse audit for URL: {url}\n'
                          f'Error: {e.stderr}')
            return False

        return True

    def audit_exists(self, filename):
        """
        Check if the audit JSON file exists.

        Args:
            filename (str): The name of the audit file (without extension).

        Returns:
            bool: True if the audit JSON file exists, False otherwise.
        """
        audit_json = os.path.join(self.output_directory, f"{filename}.json")

        if os.path.isfile(audit_json):
            return True
        else:
            logging.error(f"Audit file '{audit_json}' does not exist.")
            return False

    def get_audit_metrics(self, filename):
        """
        Retrieves Lighthouse audit metrics from a JSON file and returns them as
        a dictionary.

        Args:
            filename (str): The name of the JSON file (without the file
            extension).

        Returns:
            dict: A dictionary containing the audit metrics.
                - 'seo_score': The SEO score as a percentage.
                - 'accessibility_score': The accessibility score as a
                percentage.
                - 'performance_score': The performance score as a percentage.
                - 'best_practices_score': The best practices score as a
                percentage.
                - 'first_contentful_paint': The first contentful paint time in
                milliseconds.
                - 'speed_index': The speed index value.
                - 'largest_contentful_paint': The largest contentful paint time
                in milliseconds.
                - 'cumulative_layout_shift': The cumulative layout shift value
                as a rounded string.
                - 'total_blocking_time': The total blocking time in
                milliseconds.
                - 'time_to_interactive': The time to interactive in
                milliseconds.
        """
        file_path = os.path.join(self.output_directory, f"{filename}.json")

        try:
            with open(file_path, encoding='utf-8') as json_file:
                loaded_json = json.load(json_file)
        except FileNotFoundError as e:
            logging.error(f"File not found: '{file_path}' : {e} ")
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f'Error occurred while accessing audit metrics: {e}')
        except Exception as e:
            logging.exception(f'An unexpected error occurred: {e}')

        try:
            lighthouse_metrics = {
                'seo_score': str(round(loaded_json["categories"]["seo"]["score"] * 100)),
                'accessibility_score': str(round(loaded_json["categories"]["accessibility"]["score"] * 100)),
                'performance_score': str(round(loaded_json["categories"]["performance"]["score"] * 100)),
                'best_practices_score': str(round(loaded_json["categories"]["best-practices"]["score"] * 100)),
                'first_contentful_paint': loaded_json["audits"]["metrics"]["details"]["items"][0][
                    "firstContentfulPaint"],
                'speed_index': loaded_json["audits"]["metrics"]["details"]["items"][0]["speedIndex"],
                'largest_contentful_paint': loaded_json["audits"]["metrics"]["details"]["items"][0][
                    "largestContentfulPaint"],
                'cumulative_layout_shift': str(
                    round(loaded_json["audits"]["metrics"]["details"]["items"][0]["cumulativeLayoutShift"], 0)),
                'total_blocking_time': loaded_json["audits"]["metrics"]["details"]["items"][0]["totalBlockingTime"],
                'time_to_interactive': loaded_json["audits"]["metrics"]["details"]["items"][0]["interactive"]
            }

            return lighthouse_metrics

        finally:
            logging.info("Audit metrics retrieval completed.")

    def delete_audit_file(self, filename):
        """
        Delete an audit file.

        Args:
            filename (str): The name of the audit file (without extension).

        Returns:
            None
        """
        audit_file = os.path.join(self.output_directory, f"{filename}.json")

        try:
            os.remove(audit_file)
        except OSError as e:
            logging.warning(f"Error deleting the audit file '{filename}': {e}")

        return None
