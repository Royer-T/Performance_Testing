import pandas as pd


class DataDrive:
    def __init__(self, csv_source):
        """
        Initializes a DataDrive object.

        Parameters:
        - csv_source (str): The path or URL of the CSV file.

        """
        self.csv_source = csv_source

    def data_drive_cvs(self):
        """
        Reads the CSV file and returns a dictionary of URLs and their corresponding descriptions.

        Returns:
        - data_drive_dict (dict): A dictionary mapping URLs to descriptions.

        """
        data_driver_urls = pd.read_csv(self.csv_source)

        data_drive_dict = {row['URL']: row['Description'] for _, row in
                           data_driver_urls.iterrows()}

        return data_drive_dict
