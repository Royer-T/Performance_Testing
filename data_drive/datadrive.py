import csv


class DataDrive:
    def __init__(self, data_source):
        self.data_source = data_source

    def data_list_cvs(self):
        """
        Reads data from a CSV file and returns a list of URL data.

        :parameter: path to .csv file
        :return: A list of URL data, with each element representing a row from
        the CSV file.
        :rtype: list (nested list)
        """
        url_list = []

        with open(self.data_source, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read and discard the header

            for row in csv_reader:
                url_list.append(row)

        return url_list

