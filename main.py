import os

#  import packages (modules/classes)
import data_drive
import websites

#  constants
import constants

# 1. create a list of URLs to be evaluated
data_driver_csv = constants.CSV_DRIVER
csv_file_path = os.path.join(os.getcwd(), data_driver_csv)

# creating an object of the class, invokes a parameterized constructor
datadrive_instance = data_drive.datadrive.DataDrive(csv_file_path)
evaluate_url = datadrive_instance.data_list_cvs()

# 2. loop through the list of URLs
for url_list in evaluate_url:
    # this is a nested list, another loop is need to get the URL as a string
    for url in url_list:
        # 3. we need to know if the URL is 'up' if an evaluation can happen
        # creating an object of the class, invokes a parameterized constructor
        url_response = websites.website.Website(url)
        url_up = url_response.website_up()

        if url_up is False:
            # might want to log an error or something
            print(f'I am bad URL: {url}')
        else:
            # 4. let's get some metrics
            print(f'I am good URL: {url}')




print('we are here')
