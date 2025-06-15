#ifndef QUEUE
#define QUEUE

#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class Queue: public cSimpleModule {
private:
    cQueue buffer;  // Internal packet buffer
    cMessage *endServiceEvent;

    // Time
    simtime_t serviceTime;  // Duration of current packet's service time

    // Metrics
    cOutVector bufferSizeVector;  // Records queue size over time
    cOutVector packetDropVector;  // Records packet drops due to full buffer
public:
    Queue();
    virtual ~Queue();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Queue);

Queue::Queue() {
    endServiceEvent = NULL;
}

Queue::~Queue() {
    cancelAndDelete(endServiceEvent);
}

void Queue::initialize() {
    buffer.setName("buffer");
    bufferSizeVector.setName("bufferSizeV");
    packetDropVector.setName("packetDropV");
    endServiceEvent = new cMessage("endService");
}

void Queue::finish() {
}

void Queue::handleMessage(cMessage *msg) {
    // If this is the end of current service, start next one if any packets are waiting
    if (msg == endServiceEvent) {
        // If packet in buffer, send next one
        if (!buffer.isEmpty()) {
            // Dequeue packet
            cPacket *pkt = (cPacket*) buffer.pop();
            // Send packet
            send(pkt, "out");
            // Start new service
            serviceTime = pkt->getDuration();  // Service duration from packet
            // Schedule next service completion
            scheduleAt(simTime() + serviceTime, endServiceEvent);
        }
    // If this is an incoming packet
    } else if (buffer.getLength() >= par("bufferSize").intValue()) { // Check if buffer has space (buffer limit)
        // Buffer full: drop packet
        delete msg;
        this->bubble("packet dropped");
        packetDropVector.record(1);
    } else {
        // Enqueue the packet
        buffer.insert(msg);
        bufferSizeVector.record(buffer.getLength());

        // If the server is idle, start processing immediately
        if (!endServiceEvent->isScheduled()) {
            // Start the service now
            scheduleAt(simTime(), endServiceEvent);
        }
    }
}

#endif /* QUEUE */
