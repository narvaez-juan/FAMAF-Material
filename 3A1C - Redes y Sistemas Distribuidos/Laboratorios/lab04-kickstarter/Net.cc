#ifndef NET
#define NET

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>

using namespace omnetpp;

typedef enum {DATA, COUNTER} type_pkt;

class Net: public cSimpleModule {
private:
    unsigned int nodeCounter = 0;
    bool backToOrigin = false;
    cQueue dataBuffer;
public:
    Net();
    virtual ~Net();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
    virtual void handleCounterReturn(Packet* pkt);
    virtual void forwardPacket(Packet* pkt);
    virtual void bufferOrSend(Packet* pkt, int nodeIndex);
};

Define_Module(Net);

#endif /* NET */

Net::Net() {
}

Net::~Net() {
}

void Net::initialize() {
    // Create the initial COUNTER packet to count the number of nodes in the ring network
    Packet *counter = new Packet();
    int nodeIndex = getParentModule()->getIndex();
    counter->setKind(COUNTER);
    counter->setHopCount(0);
    counter->setSource(nodeIndex);
    counter->setDestination(nodeIndex);

    // Send the counter clockwise through gate 0
    send(counter, "toLnk$o", 0);
}

void Net::finish() {
}

void Net::handleMessage(cMessage *msg) {
    // All msg (events) on net are packets
    Packet *pkt = (Packet *) msg;
    int nodeIndex = getParentModule()->getIndex();
    int destination = pkt->getDestination();
    int kind = pkt->getKind();

    // The counter packet has already gone all the way around
    if (kind == COUNTER && destination == nodeIndex) {
        handleCounterReturn(pkt);
    }

    // The data packet has reached the destination node
    else if (destination == nodeIndex) {
        send(pkt, "toApp$o");
    }
    
    // Packet arrived from the link layer
    else if (pkt->arrivedOn("toLnk$i")) {
        forwardPacket(pkt);
    }

    // Packet arrived from the application layer 
    else {
        bufferOrSend(pkt, nodeIndex);
    }
}


void Net::handleCounterReturn(Packet* pkt) {
    nodeCounter = pkt->getHopCount() + 1;
    backToOrigin = true;
    delete pkt;
}

void Net::forwardPacket(Packet* pkt) {
    // If it's a COUNTER packet, increase its hop count
    if (pkt->getKind() == COUNTER) {
        pkt->setHopCount(pkt->getHopCount() + 1);
    }

    // Forward the packet to the next node
    int incomingGate = pkt->getArrivalGate()->getIndex();
    int outgoingGate = (incomingGate == 0) ? 1 : 0;
    send(pkt, "toLnk$o", outgoingGate);
}

void Net::bufferOrSend(Packet* pkt, int nodeIndex) {
    // Store packets on a buffer until we know the ring size
    dataBuffer.insert(pkt); 

    // Once we know the ring size, empties the data buffer
    if (backToOrigin) {
        while (!dataBuffer.isEmpty()) {
            Packet* data = (Packet*) dataBuffer.pop();
            int destination = data->getDestination();

            // Calculates closest side to destination node to send data packet
            int clockwiseDistance = (destination - nodeIndex + nodeCounter) % nodeCounter;
            int counterClockwiseDistance = nodeCounter - clockwiseDistance;

            // Choose direction based on shortest path (0 = clockwise, 1 = counterclockwise)
            int direction = (clockwiseDistance <= counterClockwiseDistance) ? 1 : 0;

            // Send the DATA packet in the chosen direction
            send(data, "toLnk$o", direction);
        }
        
    }
}