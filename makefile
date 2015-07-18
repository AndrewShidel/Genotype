debugBuild:
	g++ -ggdb -c -o bin/ram.o ram.cpp
	g++ -ggdb main.cpp bin/ram.o
debug: debugBuild
	ddd a.out -f ./twoPlusTwo.asm
build:
	g++ -c -o VM/bin/ram.o VM/ram.cpp
	g++ -o VM/main.out main.cpp VM/bin/ram.o
run: build
	./VM/main.out -f VM/test.asm
