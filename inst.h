// definition of an instruction

#ifndef INSTHEADER
#define INSTHEADER

enum OPCODES { LDA, LDI, STA, STI, ADD, SUB, JMP, JMZ, JMN, ALC, DLC, SYS, HLT };

struct Instruction {
	OPCODES opcode;
	int operand;
};
#endif