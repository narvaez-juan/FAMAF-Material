#ifndef LNK
#define LNK

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>

using namespace omnetpp;

class Lnk: public cSimpleModule {
private:
    cQueue buffer;

    // Events //
    cMessage *endServiceEvent;
    simtime_t serviceTime;

    // Stats //
    cOutVector bufferSizeVector;
public:
    Lnk();
    virtual ~Lnk();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Lnk);

#endif /* LNK */

Lnk::Lnk() {
    endServiceEvent = NULL;
}

Lnk::~Lnk() {
    cancelAndDelete(endServiceEvent);
}

void Lnk::initialize() {
    endServiceEvent = new cMessage("endService");
    bufferSizeVector.setName("Buffer Size");
}

void Lnk::finish() {
}

void Lnk::handleMessage(cMessage *msg) {

    if (msg == endServiceEvent) {
        if (!buffer.isEmpty()) {
            // Dequeue
            Packet* pkt = (Packet*) buffer.pop();
            bufferSizeVector.record(buffer.getLength());

            // Send
            send(pkt, "toOut$o");
            serviceTime = pkt->getDuration();
            scheduleAt(simTime() + serviceTime, endServiceEvent);
        }
    } else { // msg is a packet
        if (msg->arrivedOn("toNet$i")) {
            // Enqueue
            buffer.insert(msg);
            bufferSizeVector.record(buffer.getLength());

            // If the server is idle
            if (!endServiceEvent->isScheduled()) {
                // Start the service now
                scheduleAt(simTime() + 0, endServiceEvent);
            }
        } else {
            // msg is from out, send to net
            send(msg, "toNet$o");
        }
    }
}
