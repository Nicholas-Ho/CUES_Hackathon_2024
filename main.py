import database.data_layer
import database.food_database
import nutrient
import cat_status
from frontend_logic import user_input
from pathlib import Path
import database
import time
import threading
from frontend_logic import graphics_utils
from frontend_logic.message_manager import MessageManager
import copy
import os

# Time interval (in seconds)
dt = 0.2
my_cat = cat_status.Cat()
food_data_path = Path(__file__).parent / "database/data/restaurant_sample.csv"
user_db_path = Path(__file__).parent / "database/userdata/userdata.db"
layer = database.data_layer.DataLayer(food_data_path, user_db_path, multithreading=True)
message_manager = MessageManager("what did you eat?")

cat_data = layer.get_cat_data()
if cat_data is not None:
    (my_cat.size, my_cat.calories, my_cat.sugar, my_cat.protein, my_cat.total_fat, my_cat.saturated_fat,
        my_cat.trans_fat, my_cat.salt, my_cat.diabetes, my_cat.hbp, my_cat.cholesterol, my_cat.death, _) = cat_data
    message_manager.add_message("Cat loaded from prior session.")

def main(my_cat, dt):
    ans = layer.get_user_config()
    if ans is not None:
        message_manager.add_message("User data loaded from prior session.")
    else:
        ans = user_input.get_input_data()
        layer.set_user_config(ans)
    cal = nutrient.calories_recommended(ans["gender"], ans["height"], ans["weight"], ans["age"], ans["exercise_level"])
    ideal_cat = cat_status.Cat(calories=cal, 
                    sugar=nutrient.free_sugar(cal), 
                    protein=nutrient.protein_recommended(cal), 
                    total_fat=nutrient.total_fat_recommened(cal), 
                    saturated_fat=nutrient.saturated_fat_recommended(cal), 
                    trans_fat=5,
                    salt=6000)
    os.system('cls' if os.name == 'nt' else 'clear')
    graphics_utils.generate_graphics(my_cat, message_manager, print_output=True)
    t = 0
    update(t, my_cat, ideal_cat, dt, layer, message_manager)
    while True:
        check_food(my_cat, layer, message_manager)
    

def check_food(my_cat, layer, message_manager):
    food = input("\n")
    if food != None:
        my_cat = cat_status.cat_eat(my_cat, food, layer, message_manager)

def update(t, my_cat, ideal_cat, dt, layer, message_manager):
    old_cat = copy.deepcopy(my_cat)
    if t == 24:
        my_cat = cat_status.cat_day(my_cat, ideal_cat, layer, message_manager)
        t = 0
    my_cat = cat_status.cat_hour(my_cat, ideal_cat, layer, message_manager)

    if my_cat.equal_graphics(old_cat) == False:
        graphics_utils.generate_graphics(my_cat, message_manager, print_output=True)

    t+=1
    threading.Timer(dt, lambda: update(t, my_cat, ideal_cat, dt, layer, message_manager)).start()

if __name__ == "__main__":
    try:
        main(my_cat,dt)
    except KeyboardInterrupt:
        print("Exiting...")
        os._exit(1)