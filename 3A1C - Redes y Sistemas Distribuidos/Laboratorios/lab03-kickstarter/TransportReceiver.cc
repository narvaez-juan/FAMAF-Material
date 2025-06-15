#ifndef TRANSPORTRECEIVER

#define TRANSPORTRECEIVER

#include <string.h>
#include <omnetpp.h>

#include "Volt_m.h"

using namespace omnetpp;

/**
 * Transport layer receiver module that manages incoming Volt packets.
 *
 * This module receives Volt packets, buffers them if space is available,
 * sends acknowledgments (ACKs), and schedules packet delivery to the application layer.
 * It also implements a simple window-based flow control mechanism.
 */
class TransportReceiver : public cSimpleModule {

private:
    // ====================== Stats ====================== //
    cStdDev bufferSizeStdRec;
    cOutVector bufferSizeRec;  // Records buffer size at each change
    cOutVector packetDropRec;  // Records dropped packets due to full buffer

    cQueue buffer;  // Internal queue for storing received Volt packets

    // ====================== Events ====================== //
    cMessage *endServiceEvent;

    // ====================== Methods ====================== //
    void handleSelfMsg(cMessage * msg);
    void handleVolt(Volt * volt);
    int getCurrentWindowSize();
public:
    TransportReceiver();
    virtual ~TransportReceiver();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(TransportReceiver);

/**
 * Constructor
 */
TransportReceiver::TransportReceiver() {
    endServiceEvent = NULL;
}

/**
 * Destructor: safely cancels and deletes scheduled events.
 */
TransportReceiver::~TransportReceiver() {
    cancelAndDelete(endServiceEvent);
}

/**
 * Initialization phase: sets up statistics and creates service completion event.
 */
void TransportReceiver::initialize(){
    std::cout << "TrSender :: initialize\n";
    // Stats
    bufferSizeRec.setName("bufferSizeRec");
    bufferSizeStdRec.setName("bufferSizeRec");
    packetDropRec.setName("packetDropRec");
    packetDropRec.record(0);

    buffer.setName("buffer");

    endServiceEvent = new cMessage("endService");
    std::cout << "TrSender :: END initialize\n";
}

/**
 * Called at the end of simulation: records average buffer size.
 */
void TransportReceiver::finish(){
    // Stats record at the end of simulation
    recordScalar("Avg Buffer Size Rec", bufferSizeStdRec.getMean());
}

/**
 * Dispatches incoming messages to appropriate handlers.
 * @param msg Message triggering this handler
 */
void TransportReceiver::handleMessage(cMessage * msg) {
    if (msg->isSelfMessage()) {
        // Process internal self-message
        this->handleSelfMsg(msg);
    } else {
        // Process incoming Volt packet
        this->handleVolt((Volt*) msg);
    }
}

/**
 * Handles internal self-messages (e.g., service completion).
 * @param msg Self-message triggering this handler
 */
void TransportReceiver::handleSelfMsg(cMessage * msg) {
    if (msg == endServiceEvent) {
        if (!buffer.isEmpty()) {
            Volt * volt = (Volt *) buffer.pop();

            // Update metrics
            bufferSizeStdRec.collect(buffer.getLength());
            bufferSizeRec.record(buffer.getLength());

            // Send packet to upper layer
            send(volt, "appLayerOut");

            // Schedule next service
            simtime_t serviceTime = volt->getDuration();
            scheduleAt(simTime() + serviceTime, endServiceEvent);
        }
    }
}

/**
 * Processes incoming Volt packets and sends ACKs.
 * @param volt Pointer to the incoming Volt packet
 */
void TransportReceiver::handleVolt(Volt * volt) {
    if (buffer.getLength() < par("bufferSize").intValue()) {
        // New ACK packet
        Volt *ackVolt = new Volt("packet");

        // Set parameters ACK packet
        ackVolt->setByteLength(100); // TODO
        ackVolt->setAckFlag(true);
        ackVolt->setSeqNumber(volt->getSeqNumber());
        ackVolt->setWindowSize(getCurrentWindowSize());

        // Send ack packet
        send(ackVolt, "subnetwork$o");

        // Add packet in data queue to send
        buffer.insert(volt); // Enqueue data packet for delivery

        // Update buffer metrics
        bufferSizeStdRec.collect(buffer.getLength());
        bufferSizeRec.record(buffer.getLength());

        // If server is idle, start processing immediately
        if (!endServiceEvent->isScheduled()) {
            scheduleAt(simTime() + 0, endServiceEvent);
        }
    } else {
        // Drop packet due to full buffer
        delete(volt);
        this->bubble("volt-dropped");
        EV_INFO << "Dropping packet. Buffer full." << endl;

        // Increment dropped packets
        packetDropRec.record(1);
    }
}

/**
 * Calculates current receive window size based on remaining buffer capacity.
 * @return Current window size in bytes
 */
int TransportReceiver::getCurrentWindowSize() {
    // Calculate remaining buffer space
    int remainingBuffer = par("bufferSize").intValue() - buffer.getLength() - 2;
    remainingBuffer = remainingBuffer >= 0 ? remainingBuffer : 0;

    // Window size in bytes
    int windowSize = par("packetByteSize").intValue() * remainingBuffer;

    return windowSize;
}

#endif /* TRANSPORTRECEIVER */
