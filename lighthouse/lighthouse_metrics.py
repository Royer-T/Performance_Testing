import os
import subprocess
from constants import LIGHTHOUSE_CMD
from pathlib import Path


class LighthouseRunner:
    """
    A class for running Lighthouse audits and saving the JSON output to files.
    """

    def __init__(self, output_directory):
        """
        Initialize the LighthouseRunner instance.

        Args:
            output_directory (str): The directory where the JSON output files will be saved.
        """
        self.output_directory = output_directory

    def run_lighthouse(self, url, filename):
        """
        Run the Lighthouse audit and save the JSON output to a file.

        Args:
            url (str): The URL to run the Lighthouse audit on.
            filename (str): The desired name of the output file (without extension).
        """
        output_path = os.path.join(str(self.output_directory), filename + ".json")

        command = [
            LIGHTHOUSECMD,
            url,
            "--output=json",
            "--output-path",
            output_path,
            "--no-enable-error-reporting",
            "--no-update-notifier",
            "--quiet",
            "--preset",
            "desktop"
        ]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print("Command execution failed:", e.output)
        except FileNotFoundError:
            print("Lighthouse command not found. Please check the path.")
        except Exception as ex:
            print("An error occurred:", str(ex))