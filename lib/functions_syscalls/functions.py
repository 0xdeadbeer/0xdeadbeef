import os
import sys 
from .variables import * 
from ..global_syscall_functions import * 

def valid_function_name(name): 
    if (name[0] != "$"):
        return False

    return True

def fetch_stack(x=0):
    desired_location = (len(CALL_STACK)-1)-x
    if (desired_location < 0):
        err(f"Invalid stack index requested: '{desired_location}'")
        return []

    return CALL_STACK[desired_location] 

def dash_stack(call):
    CALL_STACK.append(call) 

def slide_stack(): 
    CALL_STACK.pop()

def call_function(params, interpreter): 
    interpreter.infunction = True 
    function_name = params[0]
    if (function_name not in LOADED_FUNCTIONS_BYNAME):
        err(f"No function with name '{function_name}' loaded.")
        return 

    function_addr = LOADED_FUNCTIONS_BYNAME[function_name]

    real_call_addr = interpreter.fetch_cursor() 
    call_addr = interpreter.fetch_cursor(1)
    func_output(real_call_addr, "Call function", f"Jumping to function '{function_name}' with address '{int_to_hex_string(function_addr)}'")
    dash_stack([[function_name, function_addr], call_addr])
    interpreter.set_cursor(function_addr)

def open_function(params, interpreter): 
    function_name = params[0]
    function_addr = interpreter.fetch_cursor(1)

    if (not valid_function_name(function_name)):
        err(f"Invalid function name '{function_name}'")
        return

    if (function_name in LOADED_FUNCTIONS_BYNAME):
        err(f"Function named '{function_name}' already declared?")
        return

    if (function_addr in LOADED_FUNCTIONS_BYADDR):
        err(f"A function already loaded at address '{int_to_hex_string(function_addr)}'?")
        return

    LOADED_FUNCTIONS_BYADDR[function_addr] = function_name
    LOADED_FUNCTIONS_BYNAME[function_name] = function_addr

    interpreter.increase_cursor() 

def ret_function(params, interpreter):
    interpreter.infunction = False

    call_record = fetch_stack()
    slide_stack()
    return_addr = call_record[1]

    func_output(interpreter.fetch_cursor(), "Ret function", f"Jumping out of the function to address '{int_to_hex_string(return_addr)}'")
    interpreter.set_cursor(return_addr)
