debugBuild:
	g++ -ggdb -c -o bin/ram.o ram.cpp
	g++ -ggdb main.cpp bin/ram.o
debug: debugBuild
	ddd a.out -f ./twoPlusTwo.asm
build:
	g++ -std=c++11 -c -o VM/bin/ram.o VM/ram.cpp
	g++ -std=c++11 -o VM/main.out VM/main.cpp VM/bin/ram.o
	g++ -std=c++11 -c -o Algorithm/bin/GA.o Algorithm/GA.cpp VM/bin/ram.o
run: build
	./VM/main.out -f VM/test.asm
buildExamples:
	g++ -std=c++11 -o Algorithm/Example Algorithm/Example.cpp VM/bin/ram.o Algorithm/bin/GA.o 

	