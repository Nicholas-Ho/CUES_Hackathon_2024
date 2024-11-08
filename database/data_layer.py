from .food_database import FoodDatabase, NutritionData
from .user_datastore import UserDatastore
import time
from pathlib import Path

class DataLayer:
    def __init__(self, food_data_path, user_db_path, multithreading=False):
        self._food_database = FoodDatabase(food_data_path)
        self._user_datastore = UserDatastore(user_db_path, not multithreading)

    # Food database
    def get_food_entry(self, item_id):
        return self._food_database.get_entry(item_id)
    
    def get_matching_food_entries_by_name(self, name):
        item_ids = self._food_database.get_id_from_name(name)
        return [self._food_database.get_entry(item_id) for item_id in item_ids]
    
    def search_food_entries(self, query, get_all=False):
        return self._food_database.search_database(query, get_all)
    
    # User datastore
    def add_food_record(self, record: NutritionData, timestamp=None):
        self._user_datastore.insert(UserDatastore.FOOD_RECORDS_TABLE,
                                    {
                                        "ItemID": record.item_id,
                                        "Timestamp": timestamp if timestamp is not None else time.time_ns()
                                    })
        
    def get_food_records(self):
        return self._user_datastore.query(UserDatastore.FOOD_RECORDS_TABLE)
    
    def set_user_config(self, user_config: dict):
        update_dict = {
            "Age": user_config["age"],
            "Gender": (user_config["gender"].upper() == 'F'),
            "Weight": user_config["weight"],
            "Height": user_config["height"],
            "ExerciseLevel": user_config["exercise_level"]
        }
        if self._user_datastore.get_table_size(UserDatastore.USER_CONFIG_TABLE) == 0:
            self._user_datastore.insert(UserDatastore.USER_CONFIG_TABLE, update_dict)
        else:
            self._user_datastore.update(UserDatastore.USER_CONFIG_TABLE, update_dict, {}, singleton=True)

    def get_user_config(self):
        result = self._user_datastore.query(UserDatastore.USER_CONFIG_TABLE)
        if len(result) > 0:
            return {
                "age": result[0][0],
                "gender": result[0][1],
                "weight": result[0][2],
                "height": result[0][3],
                "exercise_level": result[0][4],
            }
        return None
    
    def update_cat_data(self, cat):
        update_dict = {
            "Size": cat.size,
            "Calories": cat.calories,
            "Sugar": cat.sugar,
            "Protein": cat.protein,
            "TotalFat": cat.total_fat,
            "SaturatedFat": cat.saturated_fat,
            "TransFat": cat.trans_fat,
            "Salt": cat.salt,
            "Diabetes": cat.diabetes,
            "HighBloodPressure": cat.hbp,
            "Cholesterol": cat.cholesterol,
            "Death": cat.death
        }
        if self._user_datastore.get_table_size(UserDatastore.CURRENT_CAT_TABLE) == 0:
            self._user_datastore.insert(UserDatastore.CURRENT_CAT_TABLE, update_dict)
        else:
            self._user_datastore.update(UserDatastore.CURRENT_CAT_TABLE, update_dict, {}, singleton=True)

    def get_cat_data(self):
        result = self._user_datastore.query(UserDatastore.CURRENT_CAT_TABLE)
        if len(result) > 0:
            return result[0]
        return None
    

# Testing
if __name__ == "__main__":
    food_data_path = Path(__file__).parent / "data/restaurant_sample.csv"
    user_db_path = Path(__file__).parent / "userdata/userdata.db"
    layer = DataLayer(food_data_path, user_db_path)

    # Food testing
    data = layer.get_food_entry("52cdcd42051cb9eb3200680a")
    print(data.item_name)
    entries = layer.get_matching_food_entries_by_name("Corn and Black Bean Salad")
    print([entry.item_id for entry in entries])
    searched = layer.search_food_entries("ChicKen Sandwich")
    print([entry.item_name for entry in searched])