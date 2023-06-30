import json
import os
import subprocess
from constants import LIGHTHOUSE_CMD


class LighthouseRunner:
    """
    A class for running Lighthouse audits and saving the JSON output to files.
    """

    def __init__(self, output_directory):
        """
        Initialize the LighthouseRunner instance.

        Args:
            self: An instance of the class containing the method.
            output_directory (str): The directory where the JSON output files will be saved.
        """
        self.output_directory = output_directory

    def run_lighthouse(self, url, filename):
        """
        Run the Lighthouse audit and save the JSON output to a file.

        Args:
            self: An instance of the class containing the method.
            url (str): The URL to run the Lighthouse audit on.
            filename (str): The desired name of the output file (without extension).

        Returns:
            bool: True if successful, False if an error was encountered.
        """
        output_path = os.path.join(self.output_directory, f"{filename}.json")

        # Assume success initially
        success = True

        command = [
            LIGHTHOUSE_CMD,
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
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                print("Command execution failed:", stderr)
                success = False
        except FileNotFoundError:
            print("Lighthouse command not found. Please check the path.")
            success = False

        return success

    def audit_exists(self, filename):
        """
        Check if the audit JSON file exists.

        Args:
            self: An instance of the class containing the method.
            filename (str): The name of the audit file (without extension).

        Returns:
            bool: True if the audit JSON file exists, False otherwise.
        """
        audit_json = os.path.join(self.output_directory, f"{filename}.json")

        return os.path.isfile(audit_json)

    def pull_audit_metrics(self, filename):
        """
        Retrieves Lighthouse audit metrics from a JSON file and returns them as a dictionary.

        Args:
            self: An instance of the class containing the method.
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
                - 'first_contentful_paint': The first contentful paint time
                in milliseconds.
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

        with open(file_path, encoding='utf-8') as json_file:
            loaded_json = json.load(json_file)

        lighthouse_metrics = {
            'seo_score': str(round(loaded_json["categories"]["seo"]["score"] * 100)),
            'accessibility_score': str(round(loaded_json["categories"]["accessibility"]["score"] * 100)),
            'performance_score': str(round(loaded_json["categories"]["performance"]["score"] * 100)),
            'best_practices_score': str(round(loaded_json["categories"]["best-practices"]["score"] * 100)),
            'first_contentful_paint': loaded_json["audits"]["metrics"]["details"]["items"][0]["firstContentfulPaint"],
            'speed_index': loaded_json["audits"]["metrics"]["details"]["items"][0]["speedIndex"],
            'largest_contentful_paint': loaded_json["audits"]["metrics"]["details"]["items"][0]["largestContentfulPaint"],
            'cumulative_layout_shift': str(round(loaded_json["audits"]["metrics"]["details"]["items"][0]["cumulativeLayoutShift"], 0)),
            'total_blocking_time': loaded_json["audits"]["metrics"]["details"]["items"][0]["totalBlockingTime"],
            'time_to_interactive': loaded_json["audits"]["metrics"]["details"]["items"][0]["interactive"]
        }

        return lighthouse_metrics
