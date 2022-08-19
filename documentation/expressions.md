# Expressions

<i><a href="../programs/expressions.deadbeef">expressions.deadbeef</a></i>
```
0x000000F0 0x00 Let's do expressions!
0x000000F1 0x01 !first_number|10
0x000000F2 0x01 !second_number|240
0x000000F3 0x01 !output_number|0
0x000000F4 0x11 !first_number|!second_number|add|!output_number
0x000000F5 0x02 !output_number
```

The following piece of code will firstly print the text "Let's do expressions!" at the top. Then, three declarations & initializations, following an addition and a syscall to output a variable.

Basic operations like addition, subtraction, multiplication and division can all be done via the `0x11` syscall. The third parameter's possible values are: `add, sub, mul, div`.. which I think are pretty self-explanatory on what they do.

The first and second parameter are the two values on which the operation will be performed, and the last parameter (fourth) will be the output variable, or the variable that will store the output of the operation. 
