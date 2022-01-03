import re
import time
import math

calc = input("Enter quadratic equation: ")

valid_calc = False
if calc == "QUIT":
    sys.exit()
elif calc == "C":
    change_mode("CALC")
elif calc == "S":
    change_mode("SEQUENCE")
else:
    valid_calc = True

if valid_calc == True:
    letter = ""
    for char in calc:
        if char.isalpha():
            letter = char

    for char in calc:
        if char.isalpha():
            char = letter

    if calc[0] != "-":
        calc = "+"+calc
    if calc[1] == letter:
        calc = calc[0] + "1" + calc[1:]

    coef_one = re.search(f"[\+\-]{letter}[\+\-]",calc)
    if coef_one:
        calc = calc[:coef_one.span()[0]+1] + "1" + calc[coef_one.span()[1]-2:]

    first_x = calc.index(letter)
    second_x = calc.index(letter,first_x+1)
    a = calc[:first_x]
    b = (calc[first_x:second_x])[2:]
    c = (calc[second_x+1:])

    a,b,c = [char.replace(" ","") for char in (a,b,c)]
    a,b,c = [float(num) for num in (a,b,c)]

    inside_root = (b**2) - (4*a*c)
    if inside_root > 0:
        pos_top_line = (b*-1) + math.sqrt(inside_root)
        neg_top_line = (b*-1) - math.sqrt(inside_root)
        pos_root = pos_top_line / (2 * a)
        neg_root = neg_top_line / (2 * a)
        print(f"{letter} = {pos_root}\n{letter} ={neg_root}")
    else:
        print("Math Error")