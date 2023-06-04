import sqlite3


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
    connect(): Establishes a connection to the SQLite database.
    disconnect(): Closes the connection and cursor.
    execute_query(query, parameters=None): Executes a query on the database.
    fetch_data(query, parameters=None): Fetches data from the database.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Context manager entry point.

        Returns:
            SQLiteDatabase: The SQLiteDatabase instance.
        """
        self.connect()
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

    def connect(self):
        """
        Establishes a connection to the SQLite database.
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        """
        Closes the connection and cursor.
        """
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None

    def execute_query(self, query, parameters=None):
        """
        Executes a query on the SQLite database.

        Args:
        query (str): The SQL query to execute.
        parameters (tuple or None): Optional parameters to substitute in the
        query.

        Returns: True if the query executed successfully, False otherwise.
        :rtype: bool
        """
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return False

    def fetch_data(self, query, parameters=None):
        """
        Fetches data from the SQLite database.

        Args:
        query (str): The SQL query to fetch data.
        parameters (tuple or None): Optional parameters to substitute in the
        query.

        Returns:
        list: A list of tuples representing the fetched data.
        :rtype: list
        """
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return []


