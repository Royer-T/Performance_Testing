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
    # 2.1 Create an empty dictionary to store URL data
    url_data = {
        'URL': url,
        'Description': description,
        'Date': datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        'Environment': None,
        'Version': None,
        'Branch': None
    }

    # 2.2 gather version information
    # Create an object of the Info class
    url_versioning = Info(url)

    # Get the environment and versioning information
    environment = url_versioning.environment()
    version_string = url_versioning.versioning()

    if version_string is not None:
        url_data['Version'] = version_string.get('version', 'unknown')
        url_data['Branch'] = version_string.get('branch', 'unknown')

    # Update the dictionary
    url_data['Environment'] = environment











    # 3. we need to know if the URL is 'up' if an evaluation can happen
    # Create an object of the Website class
    url_response = Website()
    url_up = url_response.website_up(url)

    if url_up is False:
        # might want to log an error or something
        print(f'I am bad URL: {url}')
    else:
        # 4. let's get some curl metrics
        # Create an object of the CurlMetrics class
        curl_metrics = CurlMetrics(url)
        ttfb = curl_metrics.calculate_ttfb()

        # update the dictionary
        url_data.update(ttfb)

        # 5. let's get some Lighthouse metrics
        # Create an object of the Website class
        output_directory = LIGHTHOUSE_AUDIT
        runner = LighthouseRunner(output_directory)

        # Run the Lighthouse audit
        audit_success = runner.run_lighthouse(url, description)

        # ensure that the audit has created a .json file
        # this is needed since it was created outside the python framework
        if runner.audit_exist(description):
            print('audit is there')
        else:
            print('audit is not there')

        print('stuff')

        # 4.1 TTFB (time to first byte)
        print(f'I am good URL: {url}')
        ttfb = web_metrics.calculate_ttfb()

        # assign variables to the return values so that they can be added to the DB
        dns_lookup = ttfb['dns_lookup']
        connect_time = ttfb['connect_time']
        start_transfer_time = ttfb['start_transfer_time']
        total_time = ttfb['total_time']
        print(ttfb)

        # use Selenium and a Chromedriver instance to gather more metrics
        navigate = selenium_navigation.webdriver.ChromeDriver()
        driver = navigate.start_chrome(CHROME_EXE, CHROMEDRIVER)

        # 4.2 calculate page render time
        ttfp = web_metrics.calculate_ttfp(driver)
        print(f"Page TTFP time for {url}: {ttfp} milliseconds")

        # 4.3 calculate page load time
        page_load_time = web_metrics.calculate_page_load(driver)
        print(f"Page load time for {url}: {page_load_time} milliseconds")
        print()

        driver.quit()

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
