def create_fat_sad_cat(fatness=2):
    spaces = ' ' * int(fatness)
    fatness_sad = f"""
{spaces}/\\_/\\  
({spaces}T_T{spaces}) 
>{spaces} ^{spaces} <  
"""
    print(fatness_sad)

def create_fat_happy_cat(fatness=2):
    spaces = ' ' * int(fatness)
    fatness_happy = f"""
{spaces}/\\_/\\  
({spaces}o.o{spaces}) 
>{spaces} ^{spaces} <  
"""
    print(fatness_happy)
# print(create_fat_happy_cat())

def dead_cat(number=0):
    cat_lines = [
    "   /\\_/\\  " * number,
    "  ( x_x ) " * number,
    "   > ^ <  " * number
    ]
    print("Dead cat counter: " + str(number))
    print("\n".join(cat_lines)) 

def diabetes():
    cat_with_diabetes = r"""
                  ________________
                 /I have diabetes,\\
                 |please reduce   |
                 |sugar.          |
                  \\_______________/
    """
    print(cat_with_diabetes)

def high_blood_pressure():
    cat = r"""
                  _________________
                 / I have high blood\\
                 |pressure, please   |
                 |reduce salt intake.|
                  \\_________________/
    """
    print(cat)

def high_cholestrol():
    cat = r"""
                  _________________
                 / I have high      \\
                 |cholestrol, please |
                 |reduce fat intake. |
                  \\_________________/
    """
    print(cat)