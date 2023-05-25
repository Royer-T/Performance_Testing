import os

#  import packages (modules/classes)
import data_drive

#  constants
import constants

# create a list of URLs to be evaluated
data_driver_csv = constants.CSV_DRIVER
csv_file_path = os.path.join(os.getcwd(), data_driver_csv)

# creating an object of the class, this invokes a parameterized constructor
datadrive_instance = data_drive.datadrive.DataDrive(csv_file_path)
evaluate_url = datadrive_instance.data_list_cvs()

print('we are here')
