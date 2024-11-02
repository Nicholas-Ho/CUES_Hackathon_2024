import nutrient
import cat_class
import frontend_logic
import time

# Time interval (in seconds)
dt = 1

def main():
    ans = frontend_logic.input.get_input_data()
    cal = nutrient.calories_recommended(ans["gender"], ans["height"], ans["weight2"], ans["age"], ans["active"])
    ideal_cat = Cat(calories=cal, 
                    sugar=nutrient.free_sugar(cal), 
                    protein=nutrient.protein_recommended(cal), 
                    total_fat=nutrient.total_fat_recommened(cal), 
                    saturated_fat=nutrient.saturated_fat_recommended(cal), 
                    trans_fat=5,
                    salt=6)

    while True:
        pass
        time.sleep(dt)
    new_food = input("What did you eat?")

    
if __name__ == "__main__":
    main()