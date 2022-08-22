import os 
from ..global_syscall_functions import * 
from .variables import * 

def import_call(params, interpreter): 
    file = params[0]
    if (not interpreter.add_environment(file)): 
        err(f"Cannot import file {file} if it already exists in the interpreter's environments")
        return 

    file = open(os.path.abspath(file), "r")

