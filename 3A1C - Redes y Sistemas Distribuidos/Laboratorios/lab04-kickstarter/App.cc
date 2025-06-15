#ifndef APP
#define APP

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>

using namespace omnetpp;

class App: public cSimpleModule {
private:
    // Events //
    cMessage *sendMsgEvent;

    // Stats //
    cStdDev delayStats;
    cOutVector delayVector;
    cOutVector hopsCount; /* Number of network devices (like routers or gateways) that a data packet passes through as it travels from a source to a destination */
public:
    App();
    virtual ~App();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(App);

#endif /* APP */

App::App() {
}

App::~App() {
}

void App::initialize() {
    // If interArrivalTime for this node is higher than 0
    // initialize packet generator by scheduling sendMsgEvent
    if (par("interArrivalTime").doubleValue() != 0) {
        sendMsgEvent = new cMessage("sendEvent");
        scheduleAt(par("interArrivalTime"), sendMsgEvent);
    }

    // Initialize statistics
    delayStats.setName("TotalDelay");
    delayVector.setName("Delay");
    hopsCount.setName("Hops");
}

void App::finish() {
    // Record statistics
    recordScalar("Average delay", delayStats.getMean());
    recordScalar("Number of packets", delayStats.getCount());
}

void App::handleMessage(cMessage *msg) {
    // If msg is a sendMsgEvent, create and send new packet
    if (msg == sendMsgEvent) {
        // Create new packet
        Packet *pkt = new Packet("packet",this->getParentModule()->getIndex());
        pkt->setByteLength(par("packetByteSize"));
        pkt->setSource(this->getParentModule()->getIndex());
        pkt->setDestination(par("destination"));

        // Send to net layer
        send(pkt, "toNet$o");

        // Compute the new departure time and schedule next sendMsgEvent
        simtime_t departureTime = simTime() + par("interArrivalTime");
        scheduleAt(departureTime, sendMsgEvent);
    }
    // else, msg is a packet from net layer
    else {
        // Compute delay and record statistics
        Packet *pkt = (Packet *) msg;
        simtime_t delay = simTime() - msg->getCreationTime();
        delayStats.collect(delay);
        delayVector.record(delay);
        hopsCount.record(pkt->getHopCount());

        // Delete msg
        delete (msg);
    }

}
