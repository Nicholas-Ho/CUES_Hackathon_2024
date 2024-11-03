import nutrient
from database.data_layer import DataLayer
import time

class Cat:
    def __init__(self, size=2, happiness=True, calories=0, sugar=0, protein=0, total_fat=0, saturated_fat=0, trans_fat=0, salt=0, diabetes=0, hbp=0, cholesterol=0, death=0):
        self.size = size
        self.happiness = happiness
        self.calories = calories
        self.sugar = sugar
        self.protein = protein
        self.total_fat = total_fat
        self.saturated_fat = saturated_fat
        self.trans_fat = trans_fat
        self.salt = salt
        self.diabetes = diabetes
        self.hbp = hbp
        self.cholesterol = cholesterol
        self.death = death

    def __repr__(self):
        return (f"Cat(size={self.size}, happiness={self.happiness}, calories={self.calories}, "
                f"sugar={self.sugar}, protein={self.protein}, total_fat={self.total_fat}, "
                f"saturated_fat={self.saturated_fat}, trans_fat={self.trans_fat}, salt={self.salt})")
    
    def equal_graphics(self, old_cat):
        if self.size == old_cat.size and self.diabetes == old_cat.diabetes and self.hbp == old_cat.hbp and self.cholesterol == old_cat.cholesterol and self.death == old_cat.death:
            return True
        else:
            return False

def cat_day(cat, ideal_cat, layer):
    cat.sugar -= ideal_cat.sugar
    cat.protein -= ideal_cat.protein
    cat.total_fat -= ideal_cat.total_fat
    cat.saturated_fat -= ideal_cat.saturated_fat
    cat.trans_fat -= ideal_cat.trans_fat
    cat.salt -= ideal_cat.salt

    if cat.salt > 5 * ideal_cat.salt :
        cat.hbp += 1
    else: 
        cat.hbp = 0

    if cat.sugar > 5 * ideal_cat.sugar :
        cat.diabetes += 1
    else: 
        cat.diabetes = 0

    if cat.saturated_fat > 5 * ideal_cat.saturated_fat :
        cat.cholesterol += 1
    else: 
        cat.cholesterol = 0

    if cat.diabetes>2 or cat.hbp>2 or cat.cholesterol>2:
        dead = cat.death + 1
        cat = Cat(death = dead)

    layer.update_cat_data(cat)
    return cat
    
def cat_hour(cat, ideal_cat, layer):
    cat.calories -= ideal_cat.calories / 24
    if cat.calories < 0:
        cat.size = cat.calories // ideal_cat.calories + 3  
    else:
        cat.size = cat.calories // ideal_cat.calories + 2

    if cat.size<0:
        dead = cat.death + 1
        cat = Cat(death = dead)
    
    layer.update_cat_data(cat)
    return cat

def cat_eat(cat, food, layer: DataLayer):
    nutrition = layer.search_food_entries(food)
    if nutrition is None:
        print("Warning: no matching food entry was found! Not updating.")
        return cat

    cat.calories += nutrition.calories
    cat.sugar += nutrition.sugars
    cat.protein += nutrition.protein
    cat.total_fat += nutrition.total_fat
    cat.saturated_fat += nutrition.saturated_fat
    cat.trans_fat += nutrition.trans_fatty_acid
    cat.salt += nutrition.calories

    layer.add_food_record(nutrition, timestamp=time.time_ns())
    layer.update_cat_data(cat)

    return cat


                