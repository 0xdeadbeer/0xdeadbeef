# Hello World Example 

<i><a href="../programs/hello-world.deadbeef">hello-world.deadbeef</a></i>
```
0x000000F0 0x00 Hello World!
```

Lets look at how this ends up spitting "Hello World!" on the output once we run it...

0xdeadbeef is an "old school" designed programming language. Therefore the first hex number would be literally the "virtual" address of the whole command for the interpreter. Each command no matter how big, will have a size of 1, meaning that the next instruction should start with `0x000000F1`.

> Sequential order is a must (form F0->FFFFFFFF), any non-sequential order of the first address will result in the termination of the program.

---

## Syscalls 

Next column is the syscalls, each syscall is like a python "function".

`0x00` is an output syscall, meaning it will output whatever follows after it. <b>Multiple parameters would have to be splitted by the pipe simbol (|)</b>

More on syscalls in the future..
