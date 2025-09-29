import psycopg2
from psycopg2 import Error

class DatabaseManager:
    """
    A class to manage database connections and operations for the Railway Reservation System.

    This class handles connecting to a PostgreSQL database, executing queries, and fetching results.
    It includes error handling for connection and query execution failures.
    """

    def __init__(self):
        """
        Initialize the DatabaseManager with database connection parameters.
        """
        self.host = 'localhost'
        self.user = 'postgres'
        self.password = '2407'
        self.database = 'railway_reservation'
        self.connection = None

    def connect(self):
        """
        Establish a connection to the PostgreSQL database.

        Raises:
            Exception: If connection fails, with details of the error.
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Database connection established successfully.")
        except Error as e:
            raise Exception(f"Error connecting to database: {e}")

    def disconnect(self):
        """
        Close the database connection if it exists.

        Raises:
            Exception: If disconnection fails, with details of the error.
        """
        if self.connection:
            try:
                self.connection.close()
                print("Database connection closed successfully.")
            except Error as e:
                raise Exception(f"Error disconnecting from database: {e}")
        else:
            print("No active connection to close.")

    def execute_query(self, query, params=None):
        """
        Execute a non-SELECT query (e.g., INSERT, UPDATE, DELETE).

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to bind to the query.

        Raises:
            Exception: If query execution fails, with details of the error.
        """
        if not self.connection:
            raise Exception("No database connection. Call connect() first.")
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()  # Commit the transaction
            cursor.close()
            print("Query executed successfully.")
        except Error as e:
            self.connection.rollback()  # Rollback on error
            raise Exception(f"Error executing query: {e}")

    def fetch_all(self, query, params=None):
        """
        Execute a SELECT query and fetch all results.

        Args:
            query (str): The SQL SELECT query to execute.
            params (tuple, optional): Parameters to bind to the query.

        Returns:
            list: A list of tuples representing the query results.

        Raises:
            Exception: If query execution or fetching fails, with details of the error.
        """
        if not self.connection:
            raise Exception("No database connection. Call connect() first.")
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            raise Exception(f"Error fetching data: {e}")

    def fetch_one(self, query, params=None):
        """
        Execute a SELECT query and fetch the first result.

        Args:
            query (str): The SQL SELECT query to execute.
            params (tuple, optional): Parameters to bind to the query.

        Returns:
            tuple or None: The first row of the query result, or None if no results.

        Raises:
            Exception: If query execution or fetching fails, with details of the error.
        """
        if not self.connection:
            raise Exception("No database connection. Call connect() first.")
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            raise Exception(f"Error fetching data: {e}")