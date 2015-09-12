#include "../VM/ram.h"
#include <vector>

template <class InputType>
class GA {
public:
	GA();
	virtual InputType OnInputRequested() {return 0;}
	virtual float OnFinished(int[]) {return 0;}
	void start(const char* file);
	void start(std::string file);
	void start(std::istream* stream);
	double mutationRate;
private:
	struct Marker {
		Marker(int _start, int _length) {
			start = _start;
			length = _length;
		}
		int start;
		int length;
	};
	typedef std::vector<Marker> ProgMarkers;
	typedef std::vector<ProgMarkers> SysMarkers;
	struct Ranking {
		Ranking(int _index, int _score) {
			index = _index;
			score = _score;
		}
		int index;
		float score;
	};
	static const int numMarkers = 10;
	RAM merge(int, int, ProgMarkers&, ProgMarkers&);
	SysMarkers memMarkers;
	SysMarkers progMarkers;
	void initMarkers(int);
	void insertMarker(ProgMarkers markers, int index);
	void deleteMarker(ProgMarkers markers, int index);
	RAM mutate(int ram);
	RAM fork(int ram);
	void insertRanking(std::vector<Ranking>& ranking, Ranking item);
	int findMatch(std::vector<Ranking>& ranking, Ranking item);
	std::vector<RAM> rams;
	bool running = true;
protected:
	
};