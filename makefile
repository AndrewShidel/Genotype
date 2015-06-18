build:
	g++ -c -o bin/ram.o ram.cpp
	g++ main.cpp bin/ram.o
run: build
	./a.out
