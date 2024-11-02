from .food_database import FoodDatabase, NutritionData
from .user_datastore import UserDatastore
from ..cat_status import Cat
import time
from pathlib import Path

class DataLayer:
    def __init__(self, food_data_path, user_db_path):
        self._food_database = FoodDatabase(food_data_path)
        self._user_datastore = UserDatastore(user_db_path)

    # Food database
    def get_food_entry(self, item_id):
        return self._food_database.get_entry(item_id)
    
    def get_matching_food_entries_by_name(self, name):
        item_ids = self._food_database.get_id_from_name(name)
        return [self._food_database.get_entry(item_id) for item_id in item_ids]
    
    def search_food_entries(self, query):
        return self._food_database.search_database(query)
    
    # User datastore
    def add_food_record(self, record: NutritionData, timestamp=None):
        self._user_datastore.insert(UserDatastore.FOOD_RECORDS_TABLE,
                                    {
                                        "ItemID": record.item_id,
                                        "Timestamp": timestamp if timestamp is not None else time.time_ns()
                                    })
        
    def get_food_records(self):
        return self._user_datastore.query(UserDatastore.FOOD_RECORDS_TABLE)
    
    def set_user_config(self, age, gender, weight, height, exercise_level):
        update_dict = {
            "Age": age,
            "Gender": (gender.upper() == 'F'),
            "Weight": weight,
            "Height": height,
            "ExerciseLevel": exercise_level
        }
        if self._user_datastore.get_table_size(UserDatastore.USER_CONFIG_TABLE) == 0:
            self._user_datastore.insert(UserDatastore.USER_CONFIG_TABLE, update_dict)
        else:
            self._user_datastore.update(UserDatastore.USER_CONFIG_TABLE, update_dict, {}, singleton=True)

    def get_user_config(self):
        return self._user_datastore.query(UserDatastore.USER_CONFIG_TABLE)[0]
    
    def update_cat_data(self, cat: Cat):
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
        return self._user_datastore.query(UserDatastore.CURRENT_CAT_TABLE)[0]
    

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