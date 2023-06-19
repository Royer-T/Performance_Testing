from datetime import datetime

#  import packages (modules/classes)
from data_drive.datadrive import DataDrive
from url_information.information import Info
import metrics
import selenium_navigation
import storage
import websites

#  constants
from constants import *

# 1. create a list of URLs to be evaluated
# Create an object of the DataDrive class
data_drive_instance = DataDrive(CSV_DRIVER)

# Get the list of URLs to be evaluated
urls_to_evaluate = data_drive_instance.data_list_cvs()


# 2. loop through the list of URLs
for nested_url_list in urls_to_evaluate:
    url, *_ = nested_url_list

    # Create an object of the Info class
    url_info = Info(url)
    environment = url_info.environment()
    version_string = url_info.versioning()









    # 3. we need to know if the URL is 'up' if an evaluation can happen
    # creating an object of the class, invokes a parameterized constructor
    url_response = websites.website.Website(url)
    url_up = url_response.website_up()

    if url_up is False:
        # might want to log an error or something
        print(f'I am bad URL: {url}')
    else:
        # 4. let's get some metrics
        web_metrics = metrics.web_metrics.WebMetrics(url)

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
