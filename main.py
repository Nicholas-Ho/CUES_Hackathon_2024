import database.data_layer
import database.food_database
import nutrient
import cat_status
from frontend_logic import user_input
from pathlib import Path
import database
import time
import threading
from frontend_logic import cat

# Time interval (in seconds)
dt = 1
my_cat = cat_status.Cat()
food_data_path = Path(__file__).parent / "database/data/restaurant_sample.csv"
layer = database.data_layer.DataLayer(food_data_path)

def main(my_cat, dt):
    ans = user_input.get_input_data()
    cal = nutrient.calories_recommended(ans["gender"], ans["height"], ans["weight"], ans["age"], ans["exercise_level"])
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
            my_cat = cat_status.cat_day(my_cat, ideal_cat)
            t = 0
        my_cat = cat_status.cat_hour(my_cat, ideal_cat)

        if my_cat.death > 0:
            cat.dead_cat(my_cat.death)
        if my_cat.diabetes > 0 or my_cat.hbp > 0 or my_cat.cholesterol > 0:
            cat.create_fat_sad_cat(my_cat.size)
        if my_cat.diabetes > 0:
            cat.diabetes()
        if my_cat.hbp > 0:
            cat.high_blood_pressure()
        if my_cat.cholesterol > 0:
            cat.high_cholestrol()
        else:
            cat.create_fat_happy_cat(my_cat.size)
        t+=1
        time.sleep(dt)

def check_food(my_cat, layer):
    food = input("what did you eat?")
    if food != None:
        my_cat = cat_status.cat_eat(my_cat, food, layer)

    
if __name__ == "__main__":
    main(my_cat,dt)
    threading.Thread(target=check_food(my_cat, layer), daemon=True).start()