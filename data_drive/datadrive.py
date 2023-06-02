import csv


class DataDrive:
    def __init__(self, data_source):
        """
        Initialize a DataDrive object.

        :param data_source: Path to the CSV file.
        :type data_source: str
        """
        self.data_source = data_source

    def data_list_cvs(self):
        """
        Read data from a CSV file and return a list of URL data.

        :return: A list of URL data, with each element representing a row from
        the CSV file.
        :rtype: list (nested list)
        """
        with open(self.data_source, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row

            url_list = [row for row in csv_reader]

        return url_list
