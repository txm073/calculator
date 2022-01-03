import sys
import os
import re

def check_sequence(calc):
    symbols = [",",".","-",":"]
    find = ""
    seq = calc
    try:
        find = calc[:calc.index(":")]
        seq = calc[calc.index(":")+1:]
    except ValueError:
        pass
    
    calc = calc.replace(" ","")
    symbol_check = re.search("[^ \.:\-,0-9]",calc)
    if symbol_check:
        return False
    if calc[len(calc)-1] in symbols:
        return False
    elif calc[0] in symbols:
        return False
    if calc.count(":") > 1:
        return False
    return find,seq

def format_ans(string):
    lst = list(string)
    lst.remove("*")
    for i, x in enumerate(lst):
        if x == "1":
            if lst[i+1] == "n":
                del lst[i]
        elif x == ".":
            if lst[i+1] == "0":
                del lst[i:i+2]
        #elif x == "+":
            #   if lst[i+1] == "0":
            #      del lst[i:i+2]
    return "".join(lst)



valid_calc = False
want_term = False
while valid_calc == False:
    calc = input("Enter sequence: ")
    
    fib_search = re.search("fib\([0-9]+\)",calc)
    if fib_search:
        times = int(calc[4:-1])
        nums = [0,1]
        for i in range(times):
            nums.insert(i+2,(nums[i]+nums[i+1]))
        print(f"The {times} term in the Fibonacci sequence is {nums[times-1]}")
        print(str(nums[:-2])[1:-1])
        break

    elif calc == "QUIT":
        sys.exit()
    elif calc == "C":
        change_mode("CALC")
        break   
    elif calc == "Q":
        change_mode("QUADRATIC")
        break

    
    if check_sequence(calc) != False:
        find, seq = check_sequence(calc)
        if find != "":
            want_term = True
        if len(seq) > 2:
            valid_calc = True
        else:
            print("Sequence must have at least 3 terms")
    else:
        print("Syntax Error")

if valid_calc == True:
    seq = seq.split(",")
    for i, term in enumerate(seq):
        if term.count(".") == 0:
            seq[i] = int(term)
        else:
            seq[i] = float(term)

    diff = str(seq[1] - seq[0])
    displace = str(seq[0] - float(diff))
    if displace[0] != "-":
        displace = "+"+displace
    formula = diff+"*n"+displace
    print(f"Formula =",format_ans(formula))
    if want_term == True:
        calc = re.sub("n",find,formula)
        answer = str(eval(calc))
        if answer[len(answer)-2:] == ".0":
            answer = list(answer)
            del answer[len(answer)-2:len(answer)]
            answer = "".join(answer)
        print(f"The {find} term in the sequence = {answer}")