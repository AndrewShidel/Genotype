isLeader = false;
foundLeader = false;

while(!foundLeader) {
    if (rand() < 1/N) {
        isLeader = true; foundLeader = true;
        for (int i=0; i<N-1 && isLeader; i++) {
            send(i);
        }
    }
}



function OnMsg(int relay, String msg) {
    if (relay == 0) {
        isLeader = false;
        foundLeader = true;
    } else {
        send(relay-1);
    }
}


long myTime;
boolean isLeader;

function getLeader() {
    isLeader = true;
    myTime = time();
    send(N-1, myNum);
}

function OnMsg(int relay, long num) {
    if (num < 0) {
        if (relay>0) send(relay-1, num);
        getLeader();
        return;
    } else if (num > myTime)
        isLeader = false
    else if (isLeader && num == myTime) {
        send(N-1, -1);
    }
    if (relay>1)
        send(relay-1, num);
}




long myPos;
boolean isLeader = true;

function getLeader() {
    //Use a bijective mapping to get a unique number from x and y.
    myPos = 0.5*(gps().x + gps().y)*(gps().x + gps().y + 1) + gps().y;
    send(N-1, myPos);
}

function OnMsg(int relay, long pos) {
    if (pos > myPos)
        isLeader = false
    if (relay>1)
        send(relay-1, num);
}
