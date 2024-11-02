from pathlib import Path
import os
import sys
import sqlite3

class UserDatastore:
    LOCK_COL_NAME = "Lock"
    FOOD_RECORDS_TABLE = "FoodRecords"
    CURRENT_CAT_TABLE = "CurrentCat"
    USER_CONFIG_TABLE = "Config"
    TABLE_DEFS = {
        FOOD_RECORDS_TABLE: ["ItemID TEXT NOT NULL", "Timestamp INT NOT NULL"],
        CURRENT_CAT_TABLE: [
            "Size INT NOT NULL",
            "Calories INT NOT NULL",
            "Sugar INT NOT NULL",
            "Protein INT NOT NULL",
            "TotalFat INT NOT NULL",
            "SaturatedFat INT NOT NULL",
            "TransFat INT NOT NULL",
            "Salt INT NOT NULL",
            "Diabetes INT NOT NULL",
            "HighBloodPressure INT NOT NULL",
            "Cholesterol INT NOT NULL",
            "Death INT NOT NULL",

            # Restricting table to one row
            f"{LOCK_COL_NAME} char(1) PRIMARY KEY NOT NULL DEFAULT 'X'",
            f"CONSTRAINT Lock_Check CHECK ({LOCK_COL_NAME}='X')"
        ],
        USER_CONFIG_TABLE: [
            "Age INT NOT NULL",
            "Gender INT NOT NULL", # 0 for Male, 1 for Female
            "Weight REAL NOT NULL",
            "Height REAL NOT NULL",
            "ExerciseLevel INT NOT NULL",

            # Restricting table to one row
            f"{LOCK_COL_NAME} char(1) PRIMARY KEY NOT NULL DEFAULT 'X'",
            f"CONSTRAINT Lock_Check CHECK ({LOCK_COL_NAME}='X')"
        ]
    }

    def __init__(self, user_db_path):
        self.path = user_db_path
        self._connect_to_database()
        self._setup_database()
        self.columns = {}  # Lazy

    def _connect_to_database(self):
        Path(os.path.dirname(self.path)).mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

    def _setup_database(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  # Check for existing tables
        existing = set([entry[0] for entry in self.cursor.fetchall()])
        for name, col_defs in UserDatastore.TABLE_DEFS.items():
            if name in existing:
                continue
            self.cursor.execute(f"CREATE TABLE {name}({','.join(col_defs)});")

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def _get_table_columns(self, table):
        if table in self.columns:  # Lazy getting
            return self.columns[table]
        self.cursor.execute(f"PRAGMA table_info({table});")
        columns = [entry[1] for entry in self.cursor if entry[1] != UserDatastore.LOCK_COL_NAME]
        self.columns[table] = columns
        return columns

    def get_table_size(self, table):
        self.cursor.execute(f"SELECT COUNT(1) FROM {table}")
        return self.cursor.fetchall()[0][0]

    def query(self, table, target_cols=[], equals_conditions={}):
        columns = set(self._get_table_columns(table))
        for col in target_cols:
            if col not in columns:
                print(f"Column '{col}' not found in table '{table}'.", file=sys.stderr)
                return []
        self.cursor.execute("SELECT {} FROM {} {} {};".format(
             '*' if len(target_cols) == 0 else ','.join(target_cols),
             table,
             'WHERE' if len(equals_conditions) > 0 else '',
             ' AND '.join([f"{k}='{str(v)}'" for k,v in equals_conditions.items()])
        ))
        return self.cursor.fetchall()
    
    def insert(self, table, entry: dict):
        columns = set(self._get_table_columns(table))
        for key in entry.keys():
            if key not in columns:
                print(f"Column '{key}' not found in table '{table}'.", file=sys.stderr)
                return False
        keys = []
        values = []
        for k,v in entry.items():
            keys.append(f"'{k}'")
            values.append(f"'{str(v)}'")
        with self.connection:
            self.cursor.execute(f"INSERT INTO {table} \
                                ({','.join(keys)}) VALUES \
                                ({','.join(values)});")
            
    def update(self, table, updates: dict, equals_conditions, singleton=False):
        # Check singletons
        size = self.get_table_size(table)
        if size == 0:
            print("Nothing to update.", file=sys.stderr)
            return False
        if size > 1 and singleton:
            print("Table is not a singleton!", file=sys.stderr)
            return False
        
        # Check valid columns
        columns = set(self._get_table_columns(table))
        for col in updates.keys():
            if col not in columns:
                print(f"Column '{col}' not found in table '{table}'.", file=sys.stderr)
                return False
            
        # Update
        try:
            print("UPDATE {} SET {} {} {};".format(
                    table,
                    ','.join([f"{k}='{str(v)}'" for k,v in updates.items()]),
                    ' AND '.join([f"{k}='{str(v)}'" for k,v in equals_conditions.items()])
                ))
            with self.connection:
                self.cursor.execute("UPDATE {} SET {} {} {};".format(
                    table,
                    ','.join([f"{k}='{str(v)}'" for k,v in updates.items()]),
                    'WHERE' if not singleton else '',
                    ' AND '.join([f"{k}='{str(v)}'" for k,v in equals_conditions.items()] if not singleton else '')
                ))
        except Exception as e:
            print("SQLite Update failed with exception:", e, file=sys.stderr)
            return False
        return True


# Testing
if __name__ == "__main__":
    store = UserDatastore(Path(__file__).parent / "userdata/userdata.db")
    store.insert("FoodRecords", {"ItemID": "Foodstuffs", "Timestamp": 1000})
    store.insert("FoodRecords", {"ItemID": "More Food", "Timestamp": 200})
    store.insert("FoodRecords", {"ItemID": "Even More Food", "Timestamp": 500})
    print(store.query("FoodRecords", ["ItemID"], {"Timestamp": 200}))
    store.update("FoodRecords", {"ItemID": "Gobbled"}, {"Timestamp": 1000})
    store.update("FoodRecords", {"Timestamp": 2000}, {"ItemID": "More Food"})
    print(store.query("FoodRecords", ["Timestamp", "ItemID"], {"ItemID": "Gobbled"}))
    print(store.query("FoodRecords"))
    print(store._get_table_size("FoodRecords"))
    