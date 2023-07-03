from pathlib import Path

current_directory = Path.cwd()

CSV_DRIVER = current_directory / 'CPS_url.csv'
CHROMEDRIVER = current_directory / 'chromedriver.exe'
CHROME_EXE = Path('C:/Program Files/Google/Chrome/Application/chrome.exe')
DATABASE = current_directory / 'lighthouse_cps.db'
LIGHTHOUSE_AUDIT = current_directory / 'lighthouse_audits'
LOG_FILE = 'performance_data_errors.log'

# this will vary depending on the machine that it is run against
LIGHTHOUSE_CMD = 'C:\\Users\\Roger.Thibodeau\\AppData\\Roaming\\npm\\lighthouse.cmd'

