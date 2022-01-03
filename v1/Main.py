import re
from time import sleep
import sys
import os

PATH = "E:\\Python\\Calculator"

def change_mode(mode):
    print("\nMode:",mode)
    try:
        with open(os.path.join(PATH,"calc mode.txt"),"w") as file:
            file.write(mode)
    except FileNotFoundError:
        print("File not found!")

def check_mode():
    try:
        with open(os.path.join(PATH,"calc mode.txt"),"r") as file:
            current = str(file.read())         
            return current
    except FileNotFoundError:
        print("Unable to locate text file.")
        return "CALC"

print("Mode:",check_mode())
while True:
    mode = check_mode()
    if mode == "CALC":    
        try:
            with open(os.path.join(PATH,"Calculate.py"),"r") as file:
                source = file.read()
        except FileNotFoundError:
            print("Unable to locate required file.")
            sleep(1)
            sys.exit()
        exec(source)

    elif mode == "SEQUENCE":
        try:
            with open(os.path.join(PATH,"Sequences.py"),"r") as file:
                source = file.read()
        except FileNotFoundError:
            source = 'print("Unable to locate required file.")'
            change_mode("CALC")
        exec(source)
        
    elif mode == "QUADRATIC":
        try:
            with open(os.path.join(PATH,"Quadratic.py"),"r") as file:
                source = file.read()
        except FileNotFoundError:
            source = 'print("Unable to locate required file.")'
            change_mode("CALC")
        exec(source)
        
        