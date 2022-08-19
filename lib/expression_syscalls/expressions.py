#!/usr/bin/python3 

import os 
import sys
from .variables import * 
from ..global_syscall_functions import * 

def execute_operation(first_val, second_val, operation): 
    if (operation not in OPERATIONS): 
        err(f"No operation named '{operation}' exists")
        return None

    return OPERATIONS[operation]([first_val, second_val])

def basic_expressions(params, interpreter):

    first_val = params[0]
    second_val = params[1]
    operation = params[2]
    output_var = params[3]

    first_val = pull_value(first_val)
    second_val = pull_value(second_val)
    output = execute_operation(first_val, second_val, operation)
    push_value(output_var, output) 

    interpreter.increase_cursor() 
