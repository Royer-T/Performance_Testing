from pathlib import Path

current_directory = Path.cwd()

CSV_DRIVER = current_directory / 'CPS_url.csv'
CHROMEDRIVER = current_directory / 'chromedriver.exe'
CHROME_EXE = Path('C:/Program Files/Google/Chrome/Application/chrome.exe')
DATABASE = current_directory / 'performance_monitoring_trial.db'
LIGHTHOUSE_AUDIT = current_directory / 'lighthouse_audits'

# this will vary depending on the machine that it is run against
LIGHTHOUSE_CMD = 'C:\\Users\\RRJTh\\AppData\\Roaming\\npm\\lighthouse.cmd'

