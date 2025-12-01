import psycopg2
from psycopg2 import pool, Error
from contextlib import contextmanager
from typing import Optional, Dict, Any, List


class DatabaseConnection:
    """
    Manage conections with PostgreSQL DB.

    Uses connection pooling to optimize connection management
    and supports both individual connections and context managers.
    """

    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str,
        port: int = 5432,
        minconn: int = 1,
        maxconn: int = 20
    ):
        """
        Start the connection with PostgreSQL.

        Args:
            host: Server adress of the database
            database: Db name
            user: Access user
            password: User password
            port: Database port (default: 5432)
            minconn: Minimun of connections in the pool (default: 1)
            maxconn: Maximum of connections in the pool (default: 20)

        Raises:
            Error: If connection fails
        """
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=minconn,
                maxconn=maxconn,
                host=host,
                database=database,
                user=user,
                password=password,
                port=port
            )
        except Error as e:
            raise Error(f"Error to create a pool connection: {str(e)}") from e

    @contextmanager
    def get_connection(self):
        """
        Context manager to obtain a pool connection.

        Example:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")

        Yields:
            Connection psycopg2 object
        """
        conn = None
        try:
            conn = self.connection_pool.getconn()
            yield conn
        except Error as e:
            if conn:
                conn.rollback()
            raise Error(f"Error to obtain pool connection: {str(e)}") from e
        finally:
            if conn:
                self.connection_pool.putconn(conn)

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[tuple]:
        """
        Excute a SELECT query and returns all results.

        Args:
            query: SQL instruction
            params: Parameters for the query (to avoid SQL injection)

        Returns:
            List of tuples with the query results

        Raises:
            Error: If the execution fails
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchall()
        except Error as e:
            raise Error(f"Error to execute query: {str(e)}") from e

    def execute_query_one(self, query: str, params: Optional[tuple] = None) -> Optional[tuple]:
        """
        Execute a SELECT query and returns only the first result.

        Args:
            query: SQL Instruction
            params: Parameters for the query

        Returns:
            Single row of the query or None if no results

        Raises:
            Error: If the execution fails
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchone()
        except Error as e:
            raise Error(f"Error to execute query: {str(e)}") from e

    def execute_query_dict(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and returns results as dictionaries.

        Args:
            query: SQL Instruction
            params: Parameters for the query

        Returns:
            List of dictionaries with the results

        Raises:
            Error: If the execution fails
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Error as e:
            raise Error(f"Error to execute query: {str(e)}") from e

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Execute a instruction INSERT, UPDATE or DELETE.

        Args:
            query: SQL Instruction
            params: Parameters for the query

        Returns:
            Number of afected rows

        Raises:
            Error: If the execution fails
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    return cursor.rowcount
        except Error as e:
            raise Error(f"Error to execute update: {str(e)}") from e

    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        Execute multiple instructions INSERT, UPDATE ou DELETE em lote.

        Args:
            query: SQL Instruction
            params_list: List of parameters tuples for each execution

        Returns:
            Total of afected rows

        Raises:
            Error: If the execution fails
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    for params in params_list:
                        cursor.execute(query, params)
                    conn.commit()
                    return cursor.rowcount
        except Error as e:
            raise Error(f"Error to execute many: {str(e)}") from e

    def close(self):
        """Close the pool connection."""
        try:
            if self.connection_pool:
                self.connection_pool.closeall()
        except Error as e:
            raise Error(f"Error to close the connection pool: {str(e)}") from e
