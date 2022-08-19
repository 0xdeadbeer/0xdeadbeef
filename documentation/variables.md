# Variables

<i><a href="../programs/variables.deadbeef">variables.deadbeef</a></i>
```
0x000000F0 0x00 hello world!
0x000000F1 0x01 a|10
0x000000F2 0x02 a
```

The first command simply output "hello world!" to the screen just like in the previous example.

`0x01` is a new syscall I introduced that is used to initialize a variable

`0x02` is also a new syscal I introduced that outputs the variable's value

And as you can see from the example above, we use the pipe (|) to pass multiple parameters to the syscall (without any spaces!). In this case the first parameter is the name of the variable, and then the value.
