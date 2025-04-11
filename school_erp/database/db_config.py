import sqlite3
import os

class DatabaseConfig:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'school_erp.db')

    def get_connection(self):
        return sqlite3.connect(self.db_path)

# Create an instance of DatabaseConfig
db_config = DatabaseConfig() 