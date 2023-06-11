from datetime import datetime

#  import packages (modules/classes)
import data_drive
import metrics
import selenium_navigation
import storage
import websites

#  constants
import constants

# 1. create a list of URLs to be evaluated
# create an object of the class, invokes a parameterized constructor
datadrive_instance = data_drive.datadrive.DataDrive(constants.CSV_DRIVER)
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
            driver = navigate.start_chrome(constants.CHROME_EXE, constants.CHROMEDRIVER)

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
            data_storage = storage.sqlite.SQLiteDatabase(constants.DATABASE)

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
