# Functions 

<i><a href="../programs/functions.deadbeef">functions.deadbeef</a></i>
```
0x000000F0 0x00 Functions example!!
0x000000F1 0x25 $function_name 
0x000000F2 0x00 FUNCTION CALL 
0x000000F3 0x23
0x000000F4 0x24 $function_name
```

Definining functions in <a href="../README.md">0xdeadbeef</a> is really easy.. You have a syscall to mark the start of a function and a syscall to mark the end of a function (aka when should i return back from where it was called).

Meet `0x25` and `0x23`. The first syscall is a function opener and it says that any command following this one, is going to be a function's code. `0x23` on the other hand though, is like a return instruction in assembly (if you're familiar with assembly). Once executed the execution cursor is going to return to the command from where the function was called and continue the execution from there (to put it simply... exit the function)

The third syscall is the calling syscall `0x24`. This one simply takes in the name of the function you want to call, and calls it. It also registers a new record inside the interpreter's stack so that the `0x23` later will know from where it was called.

<i><a href="../programs/function-nesting.deadbeef">function-nesting.deadbeef</a></i>
```
0x000000F0 0x00 Nesting functions!!
0x000000F1 0x25 $level_1
0x000000F2 0x00 LEVEL 1 OUTPUT
0x000000F3 0x23 
0x000000F4 0x25 $level_2
0x000000F5 0x24 $level_1
0x000000F6 0x00 LEVEL 2 OUTPUT 
0x000000F7 0x23
0x000000F8 0x25 $level_3
0x000000F9 0x24 $level_2
0x000000FA 0x00 LEVEL 3 OUTPUT 
0x000000FB 0x23
0x000000FC 0x24 $level_3
0x000000FD 0x00 LEVEL OUT OUTPUT 
```

Newly supported feature in 0xdeadbeef is that you can nest calls in the functions. 
