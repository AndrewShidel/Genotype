// definition of an instruction

#ifndef INSTHEADER
#define INSTHEADER

enum OPCODES { LDA, LDI, STA, STI, ADD, SUB, JMP, JMZ, JMN, ALC, DLC, HLT };

struct Instruction {
	OPCODES opcode;
	int operand;
};
#endif