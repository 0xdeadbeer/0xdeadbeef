# Syscalls

List of all the syscall codes available in the language. 

### Basic syscalls 

Those go from `0x00` to `0x10`

  - `0x00`: Output text to the screen (1 parameter) 
    - 1 parameter: text to output to the screen 
  - `0x01`: Declare & initialize variables (2 parameters)
    - 1 parameter: name of the variable
    - 2 parameter: value of the variable
  - `0x02`: Output variables (1 parameter)
    - 1 parameter: name of the variable whose value should be outputted
---

### Expression syscalls 

Those go from `0x11` to `0x20`

  - `0x11`: Basic operations with two values (4 parameters)
    - 1 parameter: first value 
    - 2 parameter: second value 
    - 3 parameter: basic operation
    - 4 parameter: output variable

#### Expression syscalls - Basic Operations 

Those can be used inside the `0x11` syscall. 

  - add: addition
  - sub: subtraction 
  - mul: multiply 
  - div: divide 

### Function Syscalls 

Those go from `0x21` to `0x30`

  - `0x23`: Syscall to return from the function (no parameters)
  - `0x24`: Syscall to call a function (1 parameter) 
    - 1 parameter: the name of the function
  - `0x25`: Syscall to open a function, commands folling are considered the function's code (1 parameter):
    - 1 parameter: name of the function 

### Loops 

Those go from `0x31` to `0x41`

  - `0x31`: Syscall to open a loop, (3 parameters)
    - 1 parameter: name of the ending label 
    - 2 parameter: times it will loop 
    - 3 parameter: the variable that will hold the index
  - `0x32`: Syscall to close a loop, (1 parameter)
    - 1 parameter: name of the ending label
