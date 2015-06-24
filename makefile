debugBuild:
	g++ -ggdb -c -o bin/ram.o ram.cpp
	g++ -ggdb main.cpp bin/ram.o
debug: debugBuild
	ddd a.out -f test.asm
build:
	g++ -c -o bin/ram.o ram.cpp
	g++ main.cpp bin/ram.o
run: build
	./a.out -f test.asm
