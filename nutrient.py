# trans fat less than 5 grams, salt less than 6 grams

def calories_recommended(gender="M", height=180, weight=70, age=30, active=1):
    """Calculate the daily calories intake"""
    # Gender M: Male, F: Female, hieght in cm, weight in kg, age in years
    if gender == "M":
        bmr = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
    else: 
        bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)

    # Active 0:little-no exercise, 1:lightly active, 2:moderlately active, 3:active, 4:extremely active
    if active == 0:
        amr = bmr * 1.2
    elif active == 1:
        amr = bmr * 1.375
    elif active == 2:
        amr = bmr * 1.55
    elif active == 3:
        amr = bmr * 1.725
    else:
        amr = bmr * 1.9

    return amr

def free_sugar(calories):
    """return the amount of free sugar intake per day in grams"""
    return 0.05 * calories / 4

def protein_recommended(weight):
    """returns the amount of proteins intake per day in grams"""
    return 0.75 * weight

def total_fat_recommened(calories):
    """return the amount of total fat intake per day in grams"""
    return 0.35 * calories / 9

def saturated_fat_recommended(calories):
    """return the amount of saturated fat intake per day in grams"""
    return 0.11 * calories / 9

