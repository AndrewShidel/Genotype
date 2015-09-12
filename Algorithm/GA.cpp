#include "GA.h"
#include "../VM/inst.h"
#include <fstream>
#include <Map>
#include <iostream>

template <class InputType>
GA<InputType>::GA() {
    mutationRate = 100;
}

template <class InputType>
void GA<InputType>::start(const char* file) {
    start(new std::ifstream(file));
}

template <class InputType>
void GA<InputType>::start(std::string file) {
    start(new std::ifstream(file.c_str()));
}

template <class InputType>
void GA<InputType>::start(std::istream *stream) {
	memMarkers = SysMarkers();
	progMarkers = SysMarkers();
	rams = std::vector<RAM>();
	running = true;

	rams.push_back(RAM());
    rams[0].init(stream);
    initMarkers(0);

    for (int i=0; i<29; i++) {
    	fork(0);
    }

    rams[0].setInput((char*) new int(OnInputRequested()));
    rams[0].execute();

    int cuttoff = 0;
    std::vector<Ranking> rankings = std::vector<Ranking>();

    while(running) {
    	if (rams.size() > 40) {
    		cuttoff++;
    	}else if (rams.size() < 20) {
    		cuttoff--;
    	}
    	for (int i=0; i<rams.size(); i++) {
    		rams[i].setInput((char*) new int(OnInputRequested()));
    		rams[i].execute();
    		float score = OnFinished(rams[i].getOutput());
    		if (score*10 < cuttoff) {
    			rams.erase(rams.begin()+i);
    		}else{
    			Ranking ranking = Ranking(i, score);

    			fork(i);
    		}
    	}
    }
}

template <class InputType>
void GA<InputType>::insertRanking(std::vector<Ranking>& ranking, Ranking item) {
	int i=0;
	int size = ranking.size();
	while(i<size && ranking[i].score > item.score && item.index != ranking[i].index) {
		i++;
	}
	if (i>=size) {
		ranking.push_back(item);
	}else if (item.index == (*ranking)[i].index) {
		ranking[i].score = ((*ranking)[i].score + item.score)/2;
	}else {
		ranking.insert((*ranking).begin() + i, item);
	}
}

template <class InputType>
int GA<InputType>::findMatch(std::vector<Ranking>& ranking, Ranking item) {

}

template <class InputType>
RAM GA<InputType>::fork(int ramNum) {
	RAM *ram = new RAM(rams[ramNum]);
	rams.push_back(*ram);
	initMarkers(rams.size()-1);
	mutate(rams.size()-1);
	return *ram;
}

template <class InputType>
RAM GA<InputType>::mutate(int ramNum) {
	// TODO: Opcode probabilities should be based on statistics (perhaps a markov chain).
	RAM ram = rams[ramNum];
	int mutations = fmod(rand(),(ram.program.size()/mutationRate));
	int mutCount = 0;
	while(mutCount < mutations) {
		int randNum = rand()%7;
		switch(randNum) {
		case 0: { //Mutate opcode
			int randIndex = rand()%ram.program.size();
			Instruction inst = ram.program[randIndex];
			inst.opcode = static_cast<OPCODES> (rand()%OP_COUNT);
			break; }
		case 1:  { //Mutate operand
			int randIndex = rand()%ram.program.size();
			Instruction inst = ram.program[randIndex];
			inst.operand += (rand()%2)*2-1; // -1 or 1
			break; }
		case 2: { // Insert new instruction
			int randIndex = rand()%ram.program.size();
			Instruction inst(static_cast<OPCODES> (rand()%OP_COUNT), rand()%2000-1000);
			ram.program.insert(ram.program.begin()+randIndex, inst);
			insertMarker(progMarkers[ramNum], randIndex);
			break; }
		case 3: { // Erase an instruction
			int randIndex = rand()%ram.program.size();
			ram.program.erase(ram.program.begin()+randIndex);
			deleteMarker(progMarkers[ramNum], randIndex);
			break; }
		case 4: { // Edit memory location
			int randIndex = rand()%ram.memory.size();
			ram.memory[randIndex] += rand()%20-10;
			break; }
		case 5: { // Insert new memory location
			int randIndex = rand()%ram.memory.size();
			ram.memory.insert(ram.memory.begin()+randIndex, rand()%2000-1000);
			insertMarker(memMarkers[ramNum], randIndex);
			break; }
		case 6: { // Delete a memory location
			int randIndex = rand()%ram.memory.size();
			ram.memory.erase(ram.memory.begin()+randIndex);
			deleteMarker(memMarkers[ramNum], randIndex);
			break; }
		}
		mutCount++;
	}
}

template <class InputType>
void GA<InputType>::initMarkers(int ramNum) {
	RAM ram = rams[ramNum];
	int span = (ram.program.size()+ram.memory.size())/numMarkers;

	progMarkers.push_back(ProgMarkers());
	ramNum = progMarkers.size() - 1;
	for (int i=0; i<ram.program.size(); i += span) {
		progMarkers[ramNum].push_back(new Marker(i, span));
	}

	memMarkers.push_back(ProgMarkers());
	ramNum = memMarkers.size() - 1;
	for (int i=0; i<ram.memory.size(); i += span) {
		memMarkers[ramNum].push_back(new Marker(i, span));
	}
}

template <class InputType>
void GA<InputType>:: insertMarker(ProgMarkers markers, int index) {
	for (int i=0; i<markers.size(); i++) {
		if (markers[i].index > index) {
			markers[i].index++;
		}else if (markers[i].index+markers[i].length > index) {
			markers[i].length++;
		}
	}
}

template <class InputType>
void GA<InputType>:: deleteMarker(ProgMarkers markers, int index) {
	for (int i=0; i<markers.size(); i++) {
		if (markers[i].index > index) {
			markers[i].index--;
		}else if (markers[i].index+markers[i].length > index) {
			markers[i].length--;
		}
	}
}

template <class InputType>
RAM GA<InputType>::merge(int ram1, int ram2, ProgMarkers& progM, ProgMarkers& memM) {
	RAM r1 = rams[ram1];
	RAM r2 = rams[ram2];
	std::vector<Instruction> program = std::vector<Instruction>(std::max(r1.program.size(), r2.program.size()));
	std::vector<int> memory = std::vector<int>(std::max(r1.memory.size(), r2.memory.size()));
	
	int ramNum = rand()%2==0?ram1:ram2;
	int i=0;
	int k = 0;
	while(progMarkers[ramNum].size() > i) {
		Marker marker = progMarkers[ramNum][i].start;
		progM.push_back(marker);
		for (int j=marker.start; j<marker.start+marker.length; j++) {
			program[k] = rams[ramNum].program[j];
			k++;
		}
		ramNum = rand()%2==0?ram1:ram2;
		i++;
	}
	while (k<program.size()) {
		program[k] = Instruction();
	}
	i=0;
	k = 0;
	while(memMarkers[ramNum].size() > i) {
		Marker marker = memMarkers[ramNum][i].start;
		memM.push_back(marker);
		for (int j=marker.start; j<marker.start+marker.length; j++) {
			memory[k] = rams[ramNum].memory[j];
			k++;
		}
		ramNum = rand()%2==0?ram1:ram2;
		i++;
	}
	while (k<memory.size()) {
		memory[k] = 0;
	}

	RAM ram = RAM();
	ram.program = program;
	ram.memory = memory;
	return ram;
}