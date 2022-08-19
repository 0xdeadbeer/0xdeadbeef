#!/usr/bin/python3

import os 
import sys

# global variables
DEFAULT_FILE_LOCATION = "./programs/variables.deadbeef"

# global functions
def err(string): 
    print (f"[0xdeadbeef error]: {string}")

def info(string):
    print (f"[0xdeadbeef info]: {string}")

def func_output(location, name, message):
    location = "0x{:08x}".format(location).upper() 
    print (f"[{location} {name}] {message}")

# interpreter global variables
INTERPRETER_VARIABLES = {}

# interpreter global functions 
def printdb(parameters, interpreter): 
    string = parameters[0]

    func_output(interpreter.cursor, "printdb", f"{string}")
    interpreter.increase_cursor()

def printvar(parameters, interpreter):
    name = parameters[0]

    if (name not in INTERPRETER_VARIABLES):
        err(f"No variable named {name}")
        return 

    variable_val = INTERPRETER_VARIABLES[name]
    func_output(interpreter.cursor, "printvar", f"'{name}'={variable_val}")
    interpreter.increase_cursor()

def setvar(parameters, interpreter):
    name = parameters[0]
    value = parameters[1]

    if (name in INTERPRETER_VARIABLES):
        err(f"Variable with name '{name}' already exists")
        return 

    INTERPRETER_VARIABLES[name] = value
    interpreter.increase_cursor()


# interpreter global variables
SYSCALLS = {
        0: { 
            "func": printdb, 
        },
        1: {
            "func": setvar,
        },
        2: {
            "func": printvar, 
        }
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
            info(f"Program exited at {str(self.cursor)}")
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
