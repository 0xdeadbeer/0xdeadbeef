#!/usr/bin/python3

import os 
import sys
from .variables import  *

def err(string): 
    print (f"[0xdeadbeef error]: {string}")

def info(string): 
    print (f"[0xdeadbeef info]: {string}")

def int_to_hex_string(number): 
    return "0x" + "{:08x}".format(number).upper()

def func_output(location, name, message): 
    location = int_to_hex_string(location) 
    print (f"[{location} {name}] {message}")

def pull_value(origin): 
    if (origin[0] == "!"):
        if (origin[1:] not in INTERPRETER_VARIABLES): 
            err(f"No variable named '{origin[1:]}' found")
            return None 

        return INTERPRETER_VARIABLES[origin[1:]]
    else:
        return origin 

def push_value(destination, value, new=False):
    if (destination[0] != "!"):
        err(f"Can only push values inside variables!")
        return 

    if (destination[1:] not in INTERPRETER_VARIABLES and not new): 
        err(f"No variable named '{destination[1:]}' found")
        return 
    
    INTERPRETER_VARIABLES[destination[1:]] = value 
