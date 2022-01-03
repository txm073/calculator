import re
import sys
from time import sleep

def check_string(calc):
    if calc.lower() == "quit":
        return True
    
    symbol_check = re.search("e(\+?\-?)",calc)
    #if symbol_check:

    symbol_check = re.search("[\+\-\*\/][\+\-\*\/][\+\-\*\/]",calc)
    if symbol_check:
        return False
    symbol_check = re.search("[\+\*\/][\+\*\/]",calc)
    if symbol_check:
        return False
    symbol_check = re.search("[^\^\.0-9\+\-\*\/()#{},e]",calc)
    if symbol_check:
        return False
    if calc.count("(") != calc.count(")"):
        return False
    if calc.count("{") != calc.count("}"):
        return False
    if calc.count(".") > 1:
        return False
    symbol_check = re.search("\)[0-9]",calc)
    if symbol_check:
        return False
    symbol_check = re.search("#[0-9]",calc)
    if symbol_check:
        return False
    return True

def indices(calc):
    while "^" in calc:
        indice_calc = re.search("\-?[0-9]+\.?[0-9]*\^\-?[0-9]+\.?[0-9]*",calc)
        indice_area = indice_calc.group()
        power_sign = indice_area.index("^")
        x = float(indice_area[:power_sign])
        y = float(indice_area[power_sign+1:])
        if show_steps:
            print(x,y)
        answer = pow(x,y)
        if show_steps:
            print(answer)
        calc = calc[:indice_calc.span()[0]]+str(answer)+calc[indice_calc.span()[1]:]
        if show_steps:
            print("replace = ",calc)
    if show_steps:
        print("indices = done")
    return calc

def evaluate(calc):
    calc = calc.replace("e+","&")
    calc = calc.replace("e-","$")
    calc = re.sub("\-\-","+",calc)
    calc = re.sub("([0-9]+\.?[0-9]*)\-([0-9]+\.?[0-9]*)",r"\1+-\2",calc)
    ops = re.split("\-?[0-9]+\.?[0-9]*",calc)
    ops = ops[1:-1] 
    nums = re.split("[\+\*\/]",calc)
    if show_steps:
        print("operations =",ops)
        print("numbers =",nums)
    for x in ops:
        if x == "&":
            del x
        elif x == "$":
            del x
    if show_steps:
        print("operations =",ops)
        print("numbers =",nums)
    nums = [str(n).replace("&","e+") for n in nums]
    nums = [str(n).replace("$","e-") for n in nums]
    nums = [float(n) for n in nums]
    if show_steps:
        print("nums =",nums)
    if "^" in calc:
        calc = indices(calc)
    while "*" in ops or "/" in ops:
        for count, operations in enumerate(ops):
            if operations == "*":
                del ops[count]
                break
            elif operations == "/":
                del ops[count]
                break
        first_num = nums[count]
        second_num = nums[count + 1]
        if show_steps:
            print('first num =',first_num)
            print('second num =',second_num)
        if operations == "*":
            answer = first_num * second_num
            if show_steps:
                print('answer =',answer)
        if operations == "/":
            answer = first_num / second_num
            if show_steps:
                print('answer now =',answer)
        del nums[count:count+2]
        nums.insert(count, answer)
        if show_steps:
            print('number list =',nums)
            print('operations list =',ops)
    answer = str(sum(nums))+" "
    final_answer = re.sub(".0 ","",answer)
    if str(final_answer) == "inf":
        final_answer = "Infinity"
    return final_answer

def root(calc):
    root_area = re.search("{[^{]*?,\-?[0-9]+\.?[0-9]*}",calc)
    sub_calc = root_area.group()[1:-1]
    if show_steps:
        print(sub_calc)
    number = evaluate(sub_calc[:sub_calc.index(",")])
    degree = evaluate(sub_calc[sub_calc.index(",")+1:])
    number = float(number)
    root = 1/float(degree)
    if show_steps:
        print("root =",root)
    answer = str(pow(number,root))
    if show_steps:
        print("sub answer =",answer)
    calc = calc[:root_area.span()[0]]+answer+calc[root_area.span()[1]:]
    return calc

def brackets(calc):
    calc = calc.replace(")(",")*(")
    while True:
        extra_brackets = re.search("\-?[0-9]+\.?[0-9]*\(\-?[0-9]+\.?[0-9]*\+\-\*\/",calc)
        bracket_mult = re.search("[0-9]\(",calc)
        if bracket_mult:
            if show_steps:
                print("bracket span = ",bracket_mult.span())
            calc = calc[:bracket_mult.span()[0]+1]+"*"+calc[bracket_mult.span()[1]-1:]
            if show_steps:
                print(calc)
        if not bracket_mult:
            break
    while "(" in calc:
        brackets_area = re.search("\([^\(]*?\)",calc)
        sub_calc = brackets_area.group()[1:-1]
        if show_steps:
            print("brackets area = ",sub_calc)
        assert(not "(" in sub_calc)
        if "{" in sub_calc:
            sub_calc = root(sub_calc)
        if "^" in sub_calc:
            sub_calc = indices(sub_calc)
        sub_answer =  evaluate(sub_calc)
        if show_steps:
            print(brackets_area.span())
        calc = calc[:brackets_area.span()[0]]+sub_answer+calc[brackets_area.span()[1]:]
        if show_steps:
            print(calc)
    return calc

show_steps = True
valid_string = False

while valid_string == False:
    calc = input("Enter a calculation: ")
    calc = calc.replace("x","*")
    calc = calc.replace("÷","/")
    calc = calc.replace(" ","")
    
    if calc == "S":
        change_mode("SEQUENCE")
        break
    
    elif calc == "Q":
        change_mode("QUADRATIC")
        break

    elif calc == "QUIT":
        sys.exit()

    else:
        valid_option = False
        while valid_option == False:
            option = input("Would you like to see the steps? ").upper()
            option = option.replace(" ","")
            if option == "YES":
                show_steps = True
                valid_option = True
            elif option == "NO":
                show_steps = False
                valid_option = True
            else:
                print("That is not an option!")
    
    if calc.lower() == "quit":
        show_steps = False
    if show_steps:
        print(calc.replace(" ", ""))
    valid_string = check_string(calc)
    if valid_string == False:
        print("Syntax Error")
    
    pi = re.search("[0-9]#",calc)
    if pi:
        if show_steps:
            print(pi.span())
        calc = calc[:pi.span()[0]+1]+"*"+calc[pi.span()[1]-1:]
        if show_steps:
            print(calc)
    double_pi = re.search("##",calc)
    while double_pi:
        calc = calc.replace("##","#*#")
        double_pi = re.search("##",calc)
    if show_steps:
        print("replaced = ",calc)
    calc = calc.replace(")#",")*#")
    calc = calc.replace("#","3.1415926536")
    try:
        if "(" in calc:
            calc = brackets(calc)
        if "{" in calc:
            calc = root(calc)
        if "^" in calc:
            calc = indices(calc)
        print(f"Answer = {evaluate(calc)}")
        sleep(1)
    except OverflowError:
        print("Calculation Error")
    except ZeroDivisionError:
        print("Undefined")
    except:
        print("Unidentified Error")