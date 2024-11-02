import database.data_layer
import database.food_database
import nutrient
import cat_status
import frontend_logic
from pathlib import Path
import database
import time
import threading

# Time interval (in seconds)
dt = 1
cat = cat_status.Cat()
food_data_path = Path(__file__).parent / "data/restaurant_sample.csv"
layer = database.data_layer.DataLayer(food_data_path)

def main():
    ans = frontend_logic.input.get_input_data()
    cal = nutrient.calories_recommended(ans["gender"], ans["height"], ans["weight2"], ans["age"], ans["active"])
    ideal_cat = cat_status.Cat(calories=cal, 
                    sugar=nutrient.free_sugar(cal), 
                    protein=nutrient.protein_recommended(cal), 
                    total_fat=nutrient.total_fat_recommened(cal), 
                    saturated_fat=nutrient.saturated_fat_recommended(cal), 
                    trans_fat=5,
                    salt=6000)
    
    t = 0
    
    while True:
        if t == 24:
            cat_status.cat_day(cat, ideal_cat)
            t = 0
        cat_status.cat_hour(cat, ideal_cat)
        time.sleep(dt)

def check_food(cat, layer):
    food = input("what did you eat?")
    if food != None:
        cat_status.cat_eat(cat, food, layer)

    
if __name__ == "__main__":
    threading.Thread(target=check_food, daemon=True).start()
    main()