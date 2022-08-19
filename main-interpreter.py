#!/usr/bin/python3

import os 
import sys

# global variables
DEFAULT_FILE_LOCATION = "./programs/expressions.deadbeef"

# global functions
def err(string): 
    print (f"[0xdeadbeef error]: {string}")

def info(string):
    print (f"[0xdeadbeef info]: {string}")

def int_to_hex_string(number): 
    return "0x" + "{:08x}".format(number).upper()

def func_output(location, name, message):
    location = int_to_hex_string(location)
    print (f"[{location} {name}] {message}")

# interpreter global functions 
def add(params):
    first = params[0]
    second = params[1]

    return ( int(first) + int(second) )

def sub(params): 
    first = params[0]
    second = params[1]

    return ( int(first) - int(second) )

def mul(params): 
    first = params[0]
    second = params[1]

    return ( int(first) * int(second) )

def div(params): 
    first = params[0]
    second = params[1] 

    return ( int(first) / int(second) )

# interpreter global variables
INTERPRETER_VARIABLES = { }
OPERATIONS = {
    "add": add,
    "sub": sub,
    "mul": mul,
    "div": div,
}

# interpreter global functions 
def pull_value(origin): 
    if (origin[0] == "!"): # its a variable
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

def printdb(parameters, interpreter): 
    string = parameters[0]

    func_output(interpreter.cursor, "printdb", f"{string}")
    interpreter.increase_cursor()

def printvar(parameters, interpreter):
    name = parameters[0]

    variable_val = pull_value(name)
    func_output(interpreter.cursor, "printvar", f"'{name}'={variable_val}")
    interpreter.increase_cursor()

def setvar(parameters, interpreter):
    name = parameters[0]
    value = parameters[1]

    push_value(name, value, True) 

    interpreter.increase_cursor()

def execute_operation(first_val, second_val, operation): 
    if (operation not in OPERATIONS):
        err(f"No operation called '{operation}' found")
        return None

    return OPERATIONS[operation]([first_val, second_val])
    
def basic_expressions(parameters, interpreter): 
    
    first_val = parameters[0]
    second_val = parameters[1]
    operation = parameters[2]
    output_var = parameters[3]

    first_val = pull_value(first_val)
    second_val = pull_value(second_val) 
    output = execute_operation(first_val, second_val, operation)
    push_value(output_var, output)

    interpreter.increase_cursor()


# interpreter global variables
SYSCALLS = {
        
        0x00: { "func": printdb }, 
        0x01: { "func": setvar },
        0x02: { "func": printvar },
        
        0x11: { "func": basic_expressions },
}

# interpreter classes
class Command:
    def __init__(self, address, syscall, parameters):
        self.address = address
        self.syscall = syscall 
        self.parameters = parameters

    def __str__(self):
        return f"Command: address {str(self.address)}, syscall: {str(self.syscall)}, parameters: {str(self.parameters)}"

class CommandsMap:
    def __init__ (self):
        self.map = {}        

    def insert_command(self, command):
        address = command.address
        if (address in self.map):
            return False
        
        self.map[address] = command 

    def load_map(self, commands_array):
        for command in commands_array: 
            if (not self.insert_command(command)):
                continue 
    
    def fetch_command(self, address):
        if (address not in self.map):
            err(f"No address '{address}' found!")
            return None
        return self.map[address]

class DBInterpreter:
    def __init__ (self, commands_map):
        self.cursor = 0x000000F0
        self.commands_map = commands_map
        self.exit = False
        self.syscalls = SYSCALLS 
    
    def set_cursor(self, new_value):
        self.cursor = new_value
        self.execute()

    def increase_cursor(self, x=1):
        new_cursor = self.cursor + x
        self.set_cursor(new_cursor) 

    def decrease_cursor(self, x=1):
        new_cursor = self.cursor - x
        self.set_cursor(new_cursor)

    def fetch_cursor(self):
        return self.cursor
    
    def execute(self):
        if (self.exit):
            err("Cannot execute code, program exited already!")
            return 

        if (self.cursor not in self.commands_map.map):
            info(f"Program exited at {int_to_hex_string(self.cursor)}")
            self.exit = True
            return 
        
        # execute command 
        cursor_command = self.commands_map.fetch_command(self.cursor)
        cursor_syscall = cursor_command.syscall
        parameters = cursor_command.parameters
        self.syscalls[cursor_syscall]["func"](parameters, self)

# main function
def main():
    file_location = input("Enter location of program to interpret: ")
    file_location = file_location.strip() 

    if (file_location == ""):
        file_location = DEFAULT_FILE_LOCATION

    deadbeef_file = open(file_location, "r")
    commands_map = CommandsMap()
    for command in deadbeef_file:
        command = command.strip()
        command = command.split(" ")

        address = command[0]
        syscall = command[1]
        parameters = []

        if (len(command) > 2):
            parameters_string = " ".join(command[2:])
            parameters = parameters_string.split("|")
        
        address = int(address, 16)
        syscall = int(syscall, 16)
        command = Command(address, syscall, parameters)
        commands_map.insert_command(command)

        # print (f" - address: {address}, syscall: {syscall}, parameters: {str(parameters)}")

    interpreter = DBInterpreter(commands_map) 
    interpreter.execute()


if __name__ == "__main__":
    main() 
