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