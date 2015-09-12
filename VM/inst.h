// definition of an instruction

#ifndef INSTHEADER
#define INSTHEADER

const int OP_COUNT = 15;
enum OPCODES { LDA, LDI, STA, STI, ADD, SUB, JMP, JMZ, JMN, JAL, ALC, DLC, SYS, HLT, NOP };

struct Instruction {
	Instruction(OPCODES _opcode, int _operand) {
		opcode = _opcode;
		operand = _operand;
	}
	Instruction() {
		opcode = NOP;
		operand = 0;
	}
	OPCODES opcode;
	int operand;
};
#endif