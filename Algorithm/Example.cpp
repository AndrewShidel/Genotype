#include "GA.cpp"

class Example: public GA<int> {
public:
	Example() {
		start("");
	}
	int OnInputRequested() override {
		return 0;
	}
	float OnFinished(int data[]) override {
		return 0;
	}
};

int main() {
	Example ex = Example();
}