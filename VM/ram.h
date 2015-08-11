// Definition of RAM (random access machine) class

#include <vector>
#include <string>
#include "inst.h"

class RAM {
public:
	RAM();
	RAM(int pSize, int mSize);

	std::string toC(std::string path);
	
	void init();
	void init(std::istream *file);
	
	void execute();
	
	RAM* fork();
	
	std::string toString();
	
	void dump();


private:
	std::vector<int> memory;
	std::vector<Instruction> program;
	void printString(int memBase);
	int pc;
	int ac;
};