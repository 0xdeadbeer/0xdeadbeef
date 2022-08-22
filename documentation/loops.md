# Loops 

<i><a href="../programs/loops.deadbeef">loops.deadbeef</a></i>
```
0x000000F0 0x00 Introducing loops!!
0x000000F1 0x01 !iterator|0
0x000000F2 0x31 #loop_end|5|!iterator 
0x000000F3 0x00 HELLO FROM A LOOP
0x000000F4 0x02 !iterator
0x000000F5 0x32 #loop_end
0x000000F6 0x00 Done with the loop nice!
```

The loops again introduce a new section of syscalls. In this example we used the `0x31` and `0x32` syscalls to create a loop that will run 5 times. 

`0x31` syscall is the opening syscall for loops, it takes 3 parameters.. the first one being the label for of the end of the loop, the times it will loop, and then the iterator variable (aka the variable which will hold our index for the loop)

`0x32` syscall is the closing syscall for loops, it simply takes 1 parameter which is the closing label. This is like a marker command indicating that the code of the loop extends till this command. 

A new feature I also ported to 0xdeadbeef is that you can nest loops. Example of loop nesting is showing below here: 

<i><a href="../programs/loop-nesting.deadbeef">loop-nesting.deadbeef</a></i>
```
0x000000F0 0x00 Nesting loops!
0x000000F1 0x01 !x_iterator|0
0x000000F2 0x01 !y_iterator|0
0x000000F3 0x31 #x_loop|5|!x_iterator
0x000000F4 0x00 Hello in the x axis 
0x000000F5 0x02 !x_iterator
0x000000F6 0x31 #y_loop|4|!y_iterator
0x000000F7 0x00 Hello in the y axis 
0x000000F8 0x02 !y_iterator
0x000000F9 0x32 #y_loop
0x000000FA 0x32 #y_loop
0x000000FB 0x00 Exited the two nested loops!
```
