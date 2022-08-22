#!/usr/bin/python3 

import os 
import sys
from .variables import * 
from ..global_syscall_functions import * 

def printdb(parameters, interpreter): 
    string = parameters[0] 

    func_output(interpreter.cursor, "printdb", f"{string}")

def printvar(parameters, interpreter): 
    name = parameters[0] 

    variable_val = pull_value(name)
    func_output(interpreter.cursor, "printvar", f"'{name[1:]}'={variable_val}")

def setvar(parameters, interpreter):
    name = parameters[0]
    value = parameters[1]

    push_value(name, value, True) 

def program_exit(parameters, interpreter): 
    interpreter.exit = True 
