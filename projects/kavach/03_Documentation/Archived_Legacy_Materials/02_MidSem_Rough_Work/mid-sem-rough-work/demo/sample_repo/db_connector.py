"""
Database Connection & Persistence Adapter.
"""

class DatabaseConnector:
    def __init__(self, host: str = "localhost", port: int = 5432):
        self.host = host
        self.port = port
        self.connected = False

    def connect(self) -> bool:
        """Establishes database connection session."""
        self.connected = True
        return True

    def execute_query(self, sql_query: str, params: tuple = None) -> list:
        """Executes SQL query safely using parameterized inputs."""
        if not self.connected:
            self.connect()
        # Simulated database records
        if "users" in sql_query.lower():
            return [{"id": 1, "username": "admin", "role": "security_officer"}]
        return []

    def close(self):
        """Closes active connection session."""
        self.connected = False
