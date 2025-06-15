#ifndef __SLIDINGWINDOW_H
#define __SLIDINGWINDOW_H

#include <omnetpp.h>
#include "Volt_m.h"

using namespace omnetpp;

struct __packetMetadata {
    Volt * volt;
    int ackCounter;
    double sendTime = 0.0;
    bool retransmitted = false;
};

typedef struct __packetMetadata _packetMetadata;
typedef _packetMetadata * packetMetadata;

class SlidingWindow {
private:
    int baseWindow = 0;
    int bytesInFlight = 0;
    std::map<int, packetMetadata> slidingWindow;
public:
    SlidingWindow();
    virtual ~SlidingWindow();

    int getAck(int seqN);
    void addAck(int seqN);
    void addVolt(Volt * volt);
    Volt * popVolt(int seqN);
    Volt * dupVolt(int seqN);
    bool isVoltInWindow(int seqN);
    double getSendTime(int seqN);
    void addSendTime(int seqN, double time);
    int getBaseWindow();
    void setBaseWindow(int base);
    int amountBytesInFlight();
protected:
};

#endif // ifndef __SLIDINGWINDOW_H
