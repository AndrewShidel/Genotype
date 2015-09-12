#include <iostream>
#include <string>
#include <fstream>
#include "ram.h"
#include "inst.h"
using namespace std;

int main(int argc, char** argv)
{
	string fName;
	string cPath = "";
	bool usingPipe = true;
	bool run = false;

	for (int i=1; i<argc; i++) {
		if (strcmp(argv[i],"-f")==0) {
			fName = argv[++i];
			usingPipe = false;
		} else if (strcmp(argv[i],"-c")==0) {
			cPath = argv[++i];
		} else if (strcmp(argv[i],"-r")==0) {
			run = true;
		}
	}

	RAM M = RAM();
	if (usingPipe) {
		M.init(&cin);
	} else {
		M.init(new ifstream(fName.c_str()));
	}

	if (run) {
		M.execute();
	}

	if (cPath != "") {
		M.toC(cPath);
	}
	
	return 0;
}
