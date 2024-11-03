import shutil
from collections import deque
from .message_manager import MessageManager
import sys

def create_fat_sad_cat(fatness=2):
    spaces = ' ' * int(fatness)
    fatness_sad = [
        "",
        f"{spaces}/\\_/\\  ",
        f"({spaces}T_T{spaces}) ",
        f">{spaces} ^{spaces} <  ",
        ""
    ]
    return fatness_sad

def create_fat_happy_cat(fatness=2):
    spaces = ' ' * int(fatness)
    fatness_happy = [
        "",
        f"{spaces}/\\_/\\  ",
        f"({spaces}o.o{spaces}) ",
        f">{spaces} ^{spaces} <  ",
        ""
    ]
    clear_lines()
    return fatness_happy

def dead_cat(number=0):
    cat_lines = [
        " /\\_/\\    " * number,
        "( x_x )   " * number,
        " > ^ <    " * number,
        ""
    ]
    return ["Dead cat counter: " + str(number)] + cat_lines

def generate_statuses(curr_cat):
    statuses = {
        "diabetes": "sugar",
        "high blood pressure": "salt",
        "high cholesterol": "fat"
    }
    curr_statuses = []
    curr_culprits = []
    if curr_cat.diabetes > 0:
        curr_statuses.append("diabetes")
        curr_culprits.append(statuses["diabetes"])
    if curr_cat.hbp > 0:
        curr_statuses.append("high blood pressure")
        curr_culprits.append(statuses["high blood pressure"])
    if curr_cat.cholesterol > 0:
        curr_statuses.append("high cholesterol")
        curr_culprits.append(statuses["high cholesterol"])

    str_list = []
    if curr_cat.size < 1:
        str_list.append("I'm hungry")
    if len(curr_statuses) > 0:
        str_list.append("I have {}, please reduce {} intake".format(
            write_natural_list(curr_statuses),
            write_natural_list(curr_culprits)
        ))
    if len(str_list) > 0:
        text = write_natural_list(str_list)
        return generate_speech_bubble(text)
    return None

def generate_speech_bubble(content: str, width=30):
    width = max(min(width, len(content)+2), len(max(content.split(), key=lambda x: len(x)))+1)
    bubble = []
    bubble.append(' ' + '_' * (width + 1) + ' ')
    
    words = deque(content.split())
    chars_in_line = width
    curr_line = '/'
    while len(words) > 0:
        if chars_in_line < len(words[0]) + 1:
            curr_line += ' ' * chars_in_line
            curr_line += ' \\' if curr_line[0] == '/' else ' |'
            bubble.append(curr_line)
            chars_in_line = width
            curr_line = '|'
        curr_line += ' ' + words[0]
        chars_in_line -= len(words[0]) + 1
        words.popleft()
    curr_line += ' ' * chars_in_line
    curr_line += ' \\' if curr_line[0] == '/' else ' |'
    bubble.append(curr_line)

    bubble.append('\\' + '_' * (width + 1) + '/')
    return bubble

def write_natural_list(words):
    result = ""
    for i in range(len(words)-2):
        result += words[i] + ", "
    if len(words) > 1:
        result += words[-2] + " and "
    if len(words) > 0:
        result += words[-1]
    return result

def pad_lines(lines, width=30):
    for i in range(len(lines)):
        lines[i] += ' ' * max(0, width-len(lines[i]))
    return lines

def generate_graphics(curr_cat, message_manager: MessageManager, print_output=False):
    clear_lines()

    # Graveyard
    graveyard = []
    if curr_cat.death > 0:
        graveyard += dead_cat(curr_cat.death)

    # Generate cat graphics
    cat_graphics = []
    if curr_cat.diabetes > 0 or curr_cat.hbp > 0 or curr_cat.cholesterol > 0 or curr_cat.size < 1:
        cat_graphics += pad_lines(create_fat_sad_cat(curr_cat.size))
    statuses = generate_statuses(curr_cat)
    if statuses is not None:
        statuses = [""] + statuses  # padding the top
        cat_graphics += [""] * max(0, len(statuses)-len(cat_graphics))
        cat_graphics = pad_lines(cat_graphics)  # Ensuring uniform starting position
        for i in range(len(statuses)):
            cat_graphics[i] += statuses[i]

    if len(cat_graphics) == 0:
        cat_graphics = create_fat_happy_cat(curr_cat.size)
    
    graphics = graveyard + cat_graphics + message_manager.pop_messages()
    graphics_str = '\n'.join(graphics)
    if print_output:
        print(graphics_str)
    return graphics_str

def clear_lines():
    n = shutil.get_terminal_size().lines
    for _ in range(n - 1):
        print("\033[F\033[K", end='') 
    print("\033[F", end='')