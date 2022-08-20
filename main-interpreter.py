#!/usr/bin/python3

import os 
import sys
from lib import * 

# global variables
DEFAULT_FILE_LOCATION = "./programs/functions.deadbeef"
SYSCALLS = {
    0x00: printdb,
    0x01: setvar, 
    0x02: printvar, 

    0x11: basic_expressions,

    0x23: ret_function,
    0x24: call_function,
    0x25: open_function, 

    0xFF: program_exit,
}

'''
    EXCLUDE_SYSCALL_AREAS Note: 
        syscall: [ 'ignore the current syscall also', 'value for the exclude variable' ]
        ignore the current syscall also: 
            - 0x00: no 
            - 0x01: yes
'''
EXCLUDE_SYSCALL_AREAS = {
    0x23: [ 0x00, False ], 
    0x25: [ 0x01, True ], 
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
        self.excluded_areas = EXCLUDE_SYSCALL_AREAS
        self.excluding = False 
        self.infunction = False  

    def set_cursor(self, new_value):
        self.cursor = new_value
        self.execute()

    def increase_cursor(self, x=1):
        new_cursor = self.cursor + x
        self.set_cursor(new_cursor) 

    def decrease_cursor(self, x=1):
        new_cursor = self.cursor - x
        self.set_cursor(new_cursor)

    def fetch_cursor(self, x=0):
        return (self.cursor + x) 
    
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
        
        # func_output(self.cursor, "DEBUG", f"executing command {cursor_command}")
        if (cursor_syscall in self.excluded_areas):
            excluding_value = self.excluded_areas[cursor_syscall][0]

            self.excluding = excluding_value 
            if (self.excluded_areas[cursor_syscall][1] == 0x0 and not self.infunction):
                self.increase_cursor()
                return 

        elif (self.excluding):
            self.increase_cursor()
            return
        self.syscalls[cursor_syscall](parameters, self)

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
