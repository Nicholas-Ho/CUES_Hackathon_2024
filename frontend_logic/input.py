def get_input_data():
    ans={}
    while True:
        age=input("What is your age? ")
        try:
            age = int(age) 
        except ValueError:
            print("Age should be an integer")
            continue 
        if age > 150:
            print("Invalid age")
        else:
            ans["age"]=age
            break
    while True:
        gender=input("What is your gender? (M/F) ")
        if gender!="M" and gender !="F":
            continue
        else:
            ans["gender"]=gender
            break
    while True:
        weight=input("What is your weight? (kg) ")
        try:
            weight = float(weight) 
        except ValueError:
            print("Weight should be a number")
            continue 
        else:
            ans["weight"]=weight
            break
    while True:
        height=input("What is your height? (cm) ")
        try:
            height = float(height) 
        except ValueError:
            print("Height should be a number")
            continue 
        else:
            ans["height"]=height
            break
    while True:
        exercise_level=input(
        "What is your exercise level?\n"
        "0. Sedentary (Little or no exercise)\n"
        "1. Lightly active (exercise 1-3 days/week)\n"
        "2. Moderately active (exercise 3-5 days/week)\n"
        "3. Active (exercise 6-7 days/week)\n"
        "4. Extremely active (hard exercise 6-7 days/week)\n"
    )
        if exercise_level not in ["0","1","2","3","4"]:
            continue
        else:
            ans["exercise_level"]=int(exercise_level)
            break
    return ans
print(get_input_data())

