JMP 18; Check if index is in array
LDI 4;  ac <- array[i]
SUB 1;  AC <- AC - max_ele
JMN 11; AC < 0
LDI 4;  load index into ac
STA 1;  store ac in the MAX var
LDA 4;  ac <- array_index
ADD 3;  ac++
STA 4;  store current index
JMP 1;  process next item
LDA 4;  load index                  --- Begin increment index
ADD 3;  pc++
STA 4;  store index
JMP 1;  process next item
LDA 1;  load largest found          ---- Begin Halt
STI 2;  store ac as return val
HLT ;
LDA 4;  load current index          ---- Begin bound check
SUB 2;  ac <- ac - return_index
JMN 2;  jump to the beginning if negative
JMP 15; halt if >= 0
&
1   0 ; Max Size found
2   9; index of return
3   1 ; Constant 1 used for incrimenting
4   5 ; array start
5   5 ; array[1]
6   9 ; array[2]
7   35; array[3]
8   8 ; array[4]
9   0 ; location for result