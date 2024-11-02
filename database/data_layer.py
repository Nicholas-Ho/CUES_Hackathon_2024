from .food_database import FoodDatabase
from pathlib import Path

class DataLayer:
    def __init__(self, food_data_path):
        self._food_database = FoodDatabase(food_data_path)

    def get_food_entry(self, item_id):
        return self._food_database.get_entry(item_id)
    
    def get_matching_food_entries_by_name(self, name):
        item_ids = self._food_database.get_id_from_name(name)
        return [self._food_database.get_entry(item_id) for item_id in item_ids]
    
    def search_food_entries(self, query):
        return self._food_database.search_database(query)

# Testing
if __name__ == "__main__":
    food_data_path = Path(__file__).parent / "data/restaurant_sample.csv"
    layer = DataLayer(food_data_path)
    data = layer.get_food_entry("52cdcd42051cb9eb3200680a")
    print(data.item_name)
    entries = layer.get_matching_food_entries_by_name("Corn and Black Bean Salad")
    print([entry.item_id for entry in entries])
    searched = layer.search_food_entries("ChicKen Sandwich")
    print([entry.item_name for entry in searched])