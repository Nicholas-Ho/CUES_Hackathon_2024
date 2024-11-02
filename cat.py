import nutrient

class Cat:
    def __init__(self, size=2, happiness=True, calories=0, sugar=0, protein=0, total_fat=0, saturated_fat=0, trans_fat=0, salt=0):
        self.size = size
        self.happiness = happiness
        self.calories = calories
        self.sugar = sugar
        self.protein = protein
        self.total_fat = total_fat
        self.saturated_fat = saturated_fat
        self.trans_fat = trans_fat
        self.salt = salt

    def __repr__(self):
        return (f"Cat(size={self.size}, happiness={self.happiness}, calories={self.calories}, "
                f"sugar={self.sugar}, protein={self.protein}, total_fat={self.total_fat}, "
                f"saturated_fat={self.saturated_fat}, trans_fat={self.trans_fat}, salt={self.salt})")

cal = nutrient.calories_recommended(gender, height, weight, age, active)
ideal_cat = Cat(calories=cal, 
                sugar=nutrient.free_sugar(cal), 
                protein=nutrient.protein_recommended(cal), 
                total_fat=nutrient.total_fat_recommened(cal), 
                saturated_fat=nutrient.saturated_fat_recommended(cal), 
                trans_fat=5,
                salt=6)

                