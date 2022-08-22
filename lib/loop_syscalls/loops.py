from ..global_syscall_functions import *
from .variables import  *

def open_loop(params, interpreter):
    end_label = params[0]
    times = int(params[1])
    iteration_var = params[2]
    global LOOP_END

    first_loop_command = interpreter.fetch_cursor(1)
    
    for iteration in range(0, times):
        push_value(iteration_var, iteration)
        current_loop_label = LOOP_END["loop_label"] 
        while current_loop_label != end_label: 
            interpreter.increase_cursor()
            interpreter.execute()
            current_loop_label = LOOP_END["loop_label"]
        
        if (iteration < times-1):
            interpreter.set_cursor(first_loop_command) 
            interpreter.execute()

        LOOP_END = {
            "cursor": 0x0, 
            "loop_label": ""
        }

def close_loop(params, interpreter):
    end_label = params[0]
    current_cursor = interpreter.fetch_cursor()
    global LOOP_END

    LOOP_END = {
        "cursor": current_cursor, 
        "loop_label": end_label
    } 
    # func_output(current_cursor, "Close Loop", f"Reached the end of the loop {end_label}")
