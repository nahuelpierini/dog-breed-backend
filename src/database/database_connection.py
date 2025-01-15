import psycopg2
import pyodbc
from flask import current_app
from typing import Optional

class DatabaseConnection:
    """
    Class to handle connections to different database engines.
    """
    def __init__(self, engine: str, host: str, user: str, password: str, database: str):
        """
        Initialize the database connection parameters.

        :param engine: The type of database engine (e.g., 'postgresql', 'sqlserver').
        :param host: The database host address.
        :param user: The username for the database.
        :param password: The password for the database.
        :param database: The name of the database.
        """
        self.engine = engine
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self) -> Optional[object]:
        """
        Connect to the appropriate database engine based on the engine type.

        :return: A database connection object.
        :raises ValueError: If an unsupported database engine is provided.
        """
        if self.engine == "postgresql":
            return self._connect_postgresql()
        elif self.engine == "sqlserver":
            return self._connect_sqlserver()
        else:
            raise ValueError(f"Unsupported database engine: {self.engine}")

    def _connect_postgresql(self) -> psycopg2.extensions.connection:
        """
        Connect to a PostgreSQL database.

        :return: A PostgreSQL connection object.
        """
        return psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def _connect_sqlserver(self) -> pyodbc.Connection:
        """
        Connect to a SQL Server database.

        :return: A SQL Server connection object.
        """
        host=self.host,
        user=self.user,
        password=self.password,
        database=self.database
        driver = "ODBC Driver 18 for SQL Server"
        connection_string = f"Driver={driver};Server={host},1433;Database={database};Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

        return pyodbc.connect(
            connection_string
        )

    @staticmethod
    def get_connection() -> Optional[object]:
        """
        Static method to obtain a connection using the current application's configuration.

        :return: A database connection object.
        """
        config = current_app.config
        db_connection = DatabaseConnection(
            engine=config['DB_ENGINE'],
            host=config['DB_HOST'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            database=config['DB_NAME']
        )

        connection = db_connection.connect()

        print("Connection successfuly")

        return connection