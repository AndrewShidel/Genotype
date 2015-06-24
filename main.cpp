// RAM interpreter
// Purpose: To simulate the execution of a RAM (random access machine)
// Author: Jeremy Johnson
// Date: 9/25/00

#include <iostream>
#include "ram.h"
#include "inst.h"
using namespace std;

int main(int argc, char** argv)
{
	char* fName;
	/*fName = argv[2];
	for (int i=1; i<argc; i++) {
		cout << argv[i] << "\n";
	}*/
	for (int i=1; i<argc; i++) {
		cout << argv[i] << "\n";
		if (strcmp(argv[i],"-f")==0) { //Instructions
			fName = argv[++i];
		}
	}
	RAM M = RAM();
	M.init(fName);
	M.execute();
	
	return 0;
}
