import sqlite3
from typing import Any, List, Tuple, Optional

def get_db_connection():
    """Returns a connection object to the SQLite database."""
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row  # Fetch rows as dictionaries
    return connection

def execute_query(query: str, params: Optional[Tuple[Any]] = None) -> None:
    """
    Executes a query (INSERT, UPDATE, DELETE).

    :param query: SQL query to execute.
    :param params: Parameters to pass into the query (optional).
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    connection.commit()  # Commit the transaction
    connection.close()   # Close the connection

def fetch_one(query: str, params: Optional[Tuple[Any]] = None) -> Optional[sqlite3.Row]:
    """
    Fetches a single row from the database.

    :param query: SQL query to execute.
    :param params: Parameters to pass into the query (optional).
    :return: A single row (dict-like object) or None if not found.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchone()  # Fetch one result
    connection.close()
    return result

def fetch_all(query: str, params: Optional[Tuple[Any]] = None) -> List[sqlite3.Row]:
    """
    Fetches all rows from the database.

    :param query: SQL query to execute.
    :param params: Parameters to pass into the query (optional).
    :return: A list of rows (dict-like objects).
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()  # Fetch all results
    connection.close()
    return result
