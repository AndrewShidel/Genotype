// Definition of RAM (random access machine) class

#include <vector>
#include "inst.h"

class RAM {
public:
	// Constructors
	RAM();
	RAM(int pSize, int mSize);

// Initialize RAM with hardwired program and memory
// pc is set to 1 and ac is set to 0
	void init();

// Initialize RAM with program in file with the name pInput
// and initial memory configuration in the file with name mInput
// pc is set to 1 and ac is set to 0.  programSize is set to the number
// of instructions read.
	void init(const char *file);

// simulate execution of RAM with given program and memory configuration.
// Notes:
//    1. Program may not terminate (if HLT is not executed)
//    2. Currently no error checking is performed.  Checks for valid program 
//       and memory addresses and illegal opcodes should be provided.
	void execute();

// Dump memory contents
	void dump();


private:
	std::vector<char> memory;
	std::vector<Instruction> program;
	int pc;
	int ac;
};