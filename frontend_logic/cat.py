def create_fat_sad_cat(fatness=2):
    spaces = ' ' * fatness
    fatness_sad = f"""
{spaces}/\_/\  
({spaces}T_T{spaces}) 
>{spaces} ^{spaces} <  
"""
    return fatness_sad

def create_fat_happy_cat(fatness=2):
    spaces = ' ' * fatness
    fatness_happy = f"""
{spaces}/\_/\  
({spaces}o.o{spaces}) 
>{spaces} ^{spaces} <  
"""
    return fatness_happy
# print(create_fat_happy_cat())

def dead_cat(number=0):
    cat_lines = [
    "   /\_/\  " * number,
    "  ( x_x ) " * number,
    "   > ^ <  " * number
    ]
    print("Dead cat counter: " + str(number))
    return "\n".join(cat_lines)
print(dead_cat(3))

def diabetes():
    cat_with_diabetes = r"""
                  ________________
                 /I have diabetes,\
                 |please reduce   |
                 |sugar.          |
                  \_______________/
    """
    return cat_with_diabetes

def high_blood_pressure():
    cat = r"""
                  _________________
                 / I have high blood\
                 |pressure, please   |
                 |reduce salt intake.|
                  \_________________/
    """
    return cat

def high_cholestrol():
    cat = r"""
                  _________________
                 / I have high      \
                 |cholestrol, please |
                 |reduce fat intake. |
                  \_________________/
    """
    return cat