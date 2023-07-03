from pathlib import Path

current_directory = Path.cwd()

CSV_DRIVER = current_directory / 'CPS_url.csv'
DATABASE = current_directory / 'lighthouse_cps.db'
LIGHTHOUSE_AUDIT = current_directory / 'lighthouse_audits'
LOG_FILE = 'performance_data_errors.log'
