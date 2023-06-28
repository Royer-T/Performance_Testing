import datetime

#  import packages (modules/classes)
from data_driver.data_drive import DataDrive
from lighthouse.lighthouse_metrics import LighthouseRunner
from metrics.curl_metrics import CurlMetrics
from url_information.information import Info
from websites.website import Website

import selenium_navigation
import storage

#  constants
from constants import *

# 1. create a list of URLs to be evaluated
# Create an object of the DataDrive class
data_driver_csv = DataDrive(CSV_DRIVER)

# Get the list of URLs to be evaluated
urls_from_csv = data_driver_csv.data_drive_cvs()

# 2. loop through the list of URLs
for url, description in urls_from_csv.items():
    # 2.1 Create a dictionary to store URL data
    url_data = {
        'URL': url,
        'Description': description,
        'Date': datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        'Environment': None,
        'Version': 'unknown',
        'Branch': 'unknown',
        'dns_lookup': None,
        'connect_time': None,
        'start_transfer_time': None,
        'total_time': None
    }

    # 2.2 Gather version information
    # Create an object of the Info class
    url_versioning = Info(url)

    # Get the environment and versioning information
    version_info = url_versioning.versioning()

    if version_info is not None:
        url_data['Version'] = version_info.get('version', 'unknown')
        url_data['Branch'] = version_info.get('branch', 'unknown')

    # Update the dictionary with the environment
    url_data['Environment'] = url_versioning.environment()

    # 3. Check if the URL is 'up' before evaluation
    # Create an object of the Website class
    url_response = Website()
    url_up = url_response.website_up(url)

    if not url_up:
        # Log an error or handle the case where the URL is not reachable
        print(f'Error: URL is down - {url}')
        continue

    # 4. Let's get some curl metrics
    # Create an object of the CurlMetrics class
    curl_metrics = CurlMetrics(url)
    ttfb = curl_metrics.calculate_ttfb()

    url_data['dns_lookup'] = ttfb.get('dns_lookup')
    url_data['connect_time'] = ttfb.get('connect_time')
    url_data['start_transfer_time'] = ttfb.get('start_transfer_time')
    url_data['total_time'] = ttfb.get('total_time')

    # 5. let's get some Lighthouse metrics
    # Create an object of the Website class
    output_directory = LIGHTHOUSE_AUDIT
    runner = LighthouseRunner(output_directory)

    # 5.1 run the Lighthouse audit
    audit_success = runner.run_lighthouse(url, description)

    if not audit_success:
        # Log an error or handle the case where the audit was not completed
        print(f"audit for {description} in {url_data.get('Environment')} could "
              f"not be completed")
        continue

    # 5.2 ensure that the audit has created a .json file
    # this is needed since it was created outside the python framework
    audit_json_exist = runner.audit_exists(description)

    if not audit_json_exist:
        # Log an error or handle the case where the audit was not found
        print(f'{description}.json could not be found in: {LIGHTHOUSE_AUDIT}')
        continue

    print('just checking')



    if runner.audit_exist(description):
        print('audit is there')
    else:
        print('audit is not there')

    print('stuff')



    # 5. add some information to the SQLite DB
    # create an object of the class, invokes a parameterized constructor
    data_storage = storage.sqlite.SQLiteDatabase(DATABASE)

    with data_storage as db:
        insert_data_query = '''INSERT INTO cps_prod (url, occurrence, 
        dns_lookup, connect_time, start_transfer_time, total_time) VALUES (?, ?, ?, ?, ?, ?);
        '''

        # we need the current date/time
        current_datetime = datetime.now()
        session_info = (url, current_datetime, dns_lookup, connect_time,
                        start_transfer_time, total_time)

        data_storage.execute_query(insert_data_query, session_info)

print('we are here')
