import pandas as pd

class NutritionData:
    def __init__(self, series):
        # Core identifiers
        self.item_id = series["item_id"]
        self.item_name = series["item_name"]
        self.brand_id = series["brand_id"]
        self.brand_name = series["brand_name"]

        # Metadata
        self.upc = series["upc"]
        self.item_type = series["item_type"]
        self.item_description = series["item_description"]
        self.image_url = series["images_front_full_url"]
        self.last_updated = series["updated_at"]
        self.section_id = series["section_id"]

        # Serving Information
        self.servings_per_container = series["nf_servings_per_container"]
        self.serving_size_qty = series["nf_serving_size_qty"]
        self.serving_size_unit = series["nf_serving_size_unit"]
        self.serving_weight_grams = series["nf_serving_weight_grams"]

        ## Nutrition Data
        # Caloric
        self.calories = series["nf_calories"]
        self.calories_from_fat = series["nf_calories_from_fat"]

        # Fat
        self.total_fat = series["nf_total_fat"]
        self.saturated_fat = series["nf_saturated_fat"]
        self.trans_fatty_acid = series["nf_trans_fatty_acid"]
        self.polyunsaturated_fat = series["nf_polyunsaturated_fat"]
        self.monounsaturated_fat = series["nf_monounsaturated_fat"]

        # Others
        self.cholesterol = series["nf_cholesterol"]
        self.sodium = series["nf_sodium"]
        self.total_carbohydrate = series["nf_total_carbohydrate"]
        self.dietary_fiber = series["nf_dietary_fiber"]
        self.sugars = series["nf_sugars"]
        self.protein = series["nf_protein"]

        # Vitamins
        self.vitamin_a_dv = series["nf_vitamin_a_dv"]
        self.vitamin_c_dv = series["nf_vitamin_c_dv"]
        self.calcium_dv = series["nf_calcium_dv"]

        # Minerals
        self.iron_dv = series["nf_iron_dv"]
        self.potassium = series["nf_potassium"]

class FoodDatabase:
    def __init__(self, database_path):
        self.dataframe = pd.read_csv(database_path)

    def get_entry(self, item_id):
        result = self.dataframe[self.dataframe["item_id"] == item_id]
        if result.shape[0] > 1:
            print("Warning: Item ID is not unique!")
        elif result.shape[0] == 0:
            print("Item not found.")
            return
        return NutritionData(result.iloc[0])

    def get_id_from_name(self, name):
        return self.dataframe[self.dataframe["item_name"] == name]["item_id"].to_list()
    
    def search_database(self, query: str, get_all=False, search_mode="or"):
        query_terms = set([word.lower() for word in query.split()])

        # Permissive, wide search: use OR
        def condition(entries):
            result = pd.Series(False, index=range(entries.shape[0]))
            for i in range(entries.shape[0]):
                for word in entries.iloc[i].split():
                    if word.lower() in query_terms:
                        result[i] = True
            return result
        
        result = self.dataframe[condition(self.dataframe["item_name"])]
        if get_all:
            return [NutritionData(result.iloc[i]) for i in range(result.shape[0])]
        else:
            return NutritionData(result.iloc[0])