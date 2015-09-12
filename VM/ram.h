// Definition of RAM (random access machine) class

#include <vector>
#include <string>
#include "inst.h"

class RAM {
public:
	RAM();
	RAM(int pSize, int mSize);

	std::vector<int> memory;
	std::vector<Instruction> program;

	std::string toC(std::string path);
	
	void init();
	void init(std::istream *file);

	void setInput(char data[]) {};
	int* getOutput() {
		return NULL;
	}
	
	void execute();
	
	RAM fork();
	static RAM* merge(RAM, RAM);
	
	std::string toString();
	
	void dump();


private:
	void printString(int memBase);
	int pc;
	int ac;
};