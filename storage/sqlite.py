import logging
import sqlite3
from typing import List, Optional, Tuple

#  set the logging behaviour
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s '
                                                '- %(name)s:%(message)s')
logger = logging.getLogger(__name__)

class SQLiteDatabase:
    """
    A class for managing SQLite database operations.

    Args:
        db_name (str): The name of the SQLite database file.

    Attributes:
        db_name (str): The name of the SQLite database file.
        connection (sqlite3.Connection): The SQLite database connection object.
        cursor (sqlite3.Cursor): The SQLite database cursor object.

    Methods:
        execute_query(query: str, parameters: Optional[Tuple] = None) -> bool:
            Executes a query on the database.
        fetch_data(query: str, parameters: Optional[Tuple] = None) -> List[Tuple]:
            Fetches data from the database.
        insert_url_data(url_data: dict):
            Inserts URL data into the Lighthouse_CPS table.
    """

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self) -> 'SQLiteDatabase':
        """
        Context manager entry point.

        Returns:
            SQLiteDatabase: The SQLiteDatabase instance.
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point.

        Args:
            exc_type: The exception type, if any.
            exc_val: The exception value, if any.
            exc_tb: The traceback, if any.
        """
        self.disconnect()

    def disconnect(self):
        """
        Closes the connection and cursor.
        """
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None

    def execute_query(self, query: str, parameters: Optional[Tuple] = None) -> bool:
        """
        Executes a query on the SQLite database.

        Args:
            query (str): The SQL query to execute.
            parameters (tuple or None): Optional parameters to substitute in
            the query.

        Returns:
            bool: True if the query executed successfully, False otherwise.
        """
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            # Log the error message
            logging.error(f'Error executing query: {e}')
            raise

    def fetch_data(self, query: str, parameters: Optional[Tuple] = None) -> List[Tuple]:
        """
        Fetches data from the SQLite database.

        Args:
            query (str): The SQL query to fetch data.
            parameters (tuple or None): Optional parameters to substitute in
            the query.

        Returns:
            list: A list of tuples representing the fetched data.
        """
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            # Log the error message
            logging.error(f'Error fetching data: {e}')
            raise

    def insert_url_data(self, url_data: dict):
        """
        Inserts URL data into the Lighthouse_CPS table.

        Args:
            url_data (dict): A dictionary containing URL data.
        """
        url_data_keys = [
            'URL', 'Description', 'Date', 'Time', 'Environment', 'Version',
            'Branch', 'dns_lookup', 'connect_time',
            'start_transfer_time', 'total_time', 'Performance_score',
            'Accessibility_score', 'Best_Practices_score',
            'SEO_score', 'first_contentful_paint', 'speed_index',
            'largest_contentful_paint', 'cumulative_layout_shift',
            'total_blocking_time', 'time_to_interactive', 'error_log'
        ]

        # create a tuple with the values to be inserted
        session_info = tuple(url_data.get(key) for key in url_data_keys)

        # construct the insert query
        insert_data_query = '''
            INSERT INTO Lighthouse_CPS (
                url, description, date, time, environment, version, branch, 
                dns_lookup, connect_time, start_transfer_time, total_time, 
                performance_score, accessibility_score, best_practices_score, 
                seo_score, first_contentful_paint, speed_index, 
                largest_contentful_paint, cumulative_layout_shift, 
                total_blocking_time, time_to_interactive, error_log
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''

        try:
            # Execute the query
            self.execute_query(insert_data_query, session_info)
        except Exception as e:
            # Log the error message
            logging.error(f'Error inserting URL data: {e}')
            raise
