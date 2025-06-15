#ifndef GENERATOR
#define GENERATOR

#include <string.h>
#include <omnetpp.h>

#include "Volt_m.h" // Custom packet

using namespace omnetpp;

class Generator : public cSimpleModule {
private:
    /* Actual Sequence Number*/
    int currentSeqNumber;

    // Events
    cMessage *sendMsgEvent;

    // Metrics
    cStdDev transmissionStats; // Statistics collector for total number of transmissions
public:
    Generator();
    virtual ~Generator();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};
Define_Module(Generator);

Generator::Generator() {
    sendMsgEvent = NULL;

    // Set the initial sequence number
    currentSeqNumber = 0;
}

/**
 * Destructor: cancels and deletes scheduled events safely.
 */
Generator::~Generator() {
    cancelAndDelete(sendMsgEvent);
}

void Generator::initialize() {
    // Set name for statistic collection
    transmissionStats.setName("TotalTransmissions");
    // Create the send packet
    sendMsgEvent = new cMessage("sendEvent");
    // Schedule the first event at random time
    scheduleAt(par("generationInterval"), sendMsgEvent);
}

void Generator::finish() {
}

/**
 * Main logic for handling scheduled events and sending packets.
 * @param msg The message that triggered this handler
 */
void Generator::handleMessage(cMessage *msg) {
    // Create new packet
    Volt *volt;
    volt = new Volt("packet");

    // Seteamos los parametros de Volt
    volt->setByteLength(par("packetByteSize"));
    volt->setAckFlag(false);
    volt->setSeqNumber(currentSeqNumber);

    /* Increment the current sequence number, and
    when it reaches 999, it starts over from 0.
    This keeps the number within a small range (0–999) */
    currentSeqNumber = (
        currentSeqNumber + 1) % 1000;

    // Increment metric
    transmissionStats.collect(1);

    // Send to the output
    send(volt, "out");

    // Compute the new departure time
    simtime_t departureTime = simTime() + par("generationInterval");

    // Schedule the new packet generation
    scheduleAt(departureTime, sendMsgEvent);
}

#endif /* GENERATOR */
