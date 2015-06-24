JMP 18; Check if index is in array
LDI 3;  ac <- array[i]
SUB 0;  AC <- AC - max_ele
JMN 11; AC < 0
LDI 3;  load index into ac
STA 0;  store ac in the MAX var
LDA 3;  ac <- array_index
ADD 2;  ac++
STA 3;  store current index
JMP 1;  process next item
LDA 3;  load index                  --- Begin increment index
ADD 2;  pc++
STA 3;  store index
JMP 1;  process next item
LDA 0;  load largest found          ---- Begin Halt
STI 1;  store ac as return val
HLT ;
LDA 3;  load current index          ---- Begin bound check
SUB 1;  ac <- ac - return_index
JMN 2;  jump to the beginning if negative
JMP 15; halt if >= 0
HLT ;
&
0 ; Max Size found
8; index of return
1 ; Constant 1 used for incrimenting
4 ; array start
5 ; array[1]
7 ; array[2]
3; array[3]
8 ; array[4]
0 ; location for result