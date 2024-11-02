from pathlib import Path
import os
import sqlite3

class UserDatastore:
    TABLES = {
        "FoodRecords": ["ItemID TEXT NOT NULL", "Timestamp INT NOT NULL"],
        "CurrentCat": [],
        "Config": []
    }
    def __init__(self, user_db_path):
        self.path = user_db_path
        self.connect_to_database()

    def connect_to_database(self):
        Path(os.path.dirname(self.path)).mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)

    def setup_database(self):
        pass  # TODO
