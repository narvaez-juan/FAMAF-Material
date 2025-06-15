#ifndef TRANSPORTSENDER

#define TRANSPORTSENDER

#include <string.h>
#include <omnetpp.h>
#include "RenoManager.h"
#include "SlidingWindow.h"
#include "RTTManager.h"
#include "Volt_m.h"
#include "EventTimeout_m.h"

#define DUPLICATE_ACK_LIMIT 3

using namespace omnetpp;


/**
 * Transport layer sender implementing a sliding window protocol.
 *
 * This module manages the sending of data packets, handles acknowledgments,
 * controls flow using a window mechanism, and reacts to packet loss events.
 * It uses internal self-messages to schedule transmissions at regular intervals.
 */
class TransportSender : public cSimpleModule {

private:
    // ====================== Statistics Collection ====================== //
    cStdDev bufferSizeStdSen;  // Standard deviation of buffer length over time
    cOutVector bufferSizeSen;  // Records buffer size evolution over time
    cOutVector packetDropSen;  // Logs each dropped packet due to full buffer
    cStdDev packetRetransSen;  // Tracks number of retransmitted packets
    cOutVector ackTime;        // Measures RTT (Round Trip Time) from ACKs
    cOutVector rtt;

    // ====================== Internal State ====================== //
    cMessage *endServiceEvent;
    cMessage *rttEvent;
    cQueue buffer;
    std::list<int> retransmissionQueue;  // seqN

    int currentControlWindowSize;
    SlidingWindow slidingWindow;
    RenoManager renoManager;
    RTTManager rttManager;

    // ====================== Methods ====================== //
    void handleVoltToSend(Volt * volt);
    void handleSelfMsg(cMessage * msg);
    void handleVoltReceived(Volt * volt);
    void handleAck(Volt * volt);
    void handlePacketLoss(int seqN);
	void handleStartNextTransmission();
	void scheduleServiceIfIdle();
public:
    TransportSender();
    virtual ~TransportSender();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(TransportSender);

/* Constructor */
TransportSender::TransportSender() {
    rttEvent = NULL;
    endServiceEvent = NULL;

    std::cout << "TrSender :: Constructor\n";
}

/* Destructor */
TransportSender::~TransportSender() {
    cancelAndDelete(rttEvent);
    cancelAndDelete(endServiceEvent);
}

void TransportSender::initialize() {
    // Set names for statistics
    bufferSizeSen.setName("bufferSizeSen");
    bufferSizeStdSen.setName("bufferSizeSen");
    packetDropSen.setName("packetDropSen");
    packetDropSen.record(0);
    packetRetransSen.setName("packetRetransSen");
	packetRetransSen.collect(0);

	rtt.setName("ackTime");
    ackTime.setName("ackTime");
    buffer.setName("bufferSen");

    rttManager = RTTManager();
    rttEvent = new cMessage("rttEvent");

    scheduleAt(simTime() + rttManager.getCurrentRTT(), rttEvent);

    // Create and schedule the first service event
    endServiceEvent = new cMessage("endService");

    renoManager = RenoManager();
    renoManager.setSize(par("packetByteSize").intValue());

    // Initialize control window based on parameter
    slidingWindow = SlidingWindow();
    currentControlWindowSize = par("packetByteSize").intValue();

    std::cout << "TrSender :: initialize\n";
}

void TransportSender::finish() {
    // Stats record at the end of simulation

    recordScalar("Avg Buffer Size Sen", bufferSizeStdSen.getMean());
    recordScalar("Amount of Packets Retransmitted Sen", packetRetransSen.getCount());
}

void TransportSender::handleMessage(cMessage *msg) {
    if (msg->isSelfMessage()){
        // Handle internal timer events
        this->handleSelfMsg(msg);
    } else if (msg->arrivedOn("appLayerIn")) {
        // Handle new packet to send
        this->handleVoltToSend((Volt *) msg);
    } else {
        // Arrive from subnetwork
        this->handleVoltReceived((Volt *) msg);
    }
}

/**
 * Handles new packets arriving from the application layer.
 *
 * Buffers the packet and sends it when possible according to the window size.
 * Drops the packet if the buffer is full.
 *
 * @param volt Pointer to the Volt packet to be sent
 */
void TransportSender::handleVoltToSend(Volt * volt){
    // Check if there is enough space in the buffer to accept the new packet
    if (par("bufferSize").intValue() >= buffer.getLength()){
        // Buffer has space: can send packet so enqueue the incoming Volt packet
        std::cout << "TrSender :: Insert Volt\n";
        buffer.insert(volt);

        // Collect statistics on buffer usage
        bufferSizeStdSen.collect(buffer.getLength());
        bufferSizeSen.record(buffer.getLength());

        scheduleServiceIfIdle();
    } else {
        delete volt;
        this->bubble("packet-loss");

        // Update statistics on drop packets
        packetDropSen.record(1);

        // Debug console
		std::cout << "\nTrSender :: Packet Loss\n";
    }
}

void TransportSender::handleSelfMsg(cMessage * msg){
	if (msg == endServiceEvent) {
		if(!buffer.isEmpty() || !retransmissionQueue.empty()) {
			// Check the packet size without removing it from the queue
			int packetSize;

			if (buffer.isEmpty()) {
                // If the transmission buffer is empty, check if there's a packet to retransmit

                // Get sequence number of the first packet to retransmit
				int retSeqN = retransmissionQueue.front();

                // Duplicate the original Volt packet for resend
				Volt * auxVolt = slidingWindow.dupVolt(retSeqN);

                // Set size of the retransmitted packet
				packetSize = auxVolt->getByteLength();

                // Clean up the temporary packet copy (not sent yet, just used to get size)
				delete(auxVolt);
			} else {
                // Gets the first packet in the queue,
                // converts it to Volt*, and then gets its size in bytes
				packetSize = ((Volt*) buffer.front())->getByteLength();
			}

			bool hasCongestionWinEnoughSpace = renoManager.getAvailableWin() >= packetSize;
			int bytesInFlight = slidingWindow.amountBytesInFlight();

			std::cout << "TrSender :: currentControlWindowSize " << currentControlWindowSize << " bytes\n";
			std::cout << "TrSender :: current Bytes in flight " << bytesInFlight << " bytes\n";
            bool hasControlWinEnoughSpace = currentControlWindowSize - bytesInFlight >= packetSize;
			std::cout << "TrSender :: Enough Congestion Window: " << hasCongestionWinEnoughSpace;
			std::cout << "\tEnough Control Window: " << hasControlWinEnoughSpace << "\n";

            // Check if both congestion and control windows allow sending a new packet
			if (hasCongestionWinEnoughSpace && hasControlWinEnoughSpace) {
                // Send the Volt packet at the front (top) of the transmission queue
				handleStartNextTransmission();
			}
		}
	} else if (msg == rttEvent) {
//		std::cout << "TrSender :: RTT Event\n";

		if (!renoManager.getSlowStart()) {
            // Each RTT increment VC in one packet
            renoManager.setSize(renoManager.getSize() + par("packetByteSize").intValue());
        }

        scheduleAt(simTime() + rttManager.getCurrentRTT(), rttEvent);
	} else if (msg->getKind() == EVENT_TIMEOUT_KIND) {
		EventTimeout * timeout = (EventTimeout*) msg;
		std::cout << "\nTrSender :: EVENT_TIMEOUT_KIND. SeqN = " << timeout->getSeqN() << "\n";
		handlePacketLoss(timeout->getSeqN());
	}
}

/**
 * Handles incoming Volt packets (data or ACKs).
 * @param volt Pointer to the received Volt packet
*/
void TransportSender::handleVoltReceived(Volt * volt){
    // If it is an ACK packet
    if (volt->getAckFlag()) {
        handleAck(volt);
    } else {
		std::cout << "TrSender :: ERROR :: Received message through subnetwork that is not ACK\n";
	}
}

/**
 * Processes acknowledgment packets.
 *
 * - Updating sequence numbers
 *
 * - Adjusting window sizes
 *
 * - Managing timeouts and retransmissions
 *
 * @param volt Pointer to the received ACK packet
 */
void TransportSender::handleAck(Volt * volt){
    // Get Sequence Number from ACK packet
    int seqN = volt->getSeqNumber();

    // Cancel timeout
    scheduleServiceIfIdle();

    EventTimeout * timeout = renoManager.popTimeoutMsg(seqN);

	if(timeout != NULL) {
		std::cout << "Sender :: Timeout cancelled due to ACK\n";
		cancelEvent(timeout);
		delete(timeout);
		timeout = NULL;
	}

    // Update Control Window
    currentControlWindowSize = volt->getWindowSize();

    // Remove ACK packet from retransmission queue
    retransmissionQueue.remove(seqN);

    // Initialize Slow Start
    if(renoManager.getSlowStart()) {
		// We are in slow start we increase the VC to maxSize(Packet)
		renoManager.setSize(
            renoManager.getSize() + par("packetByteSize").intValue());
	}

    // Increment the ack counter by one
    slidingWindow.addAck(seqN);

    // Update RRT if is necessary
    double sendTime = slidingWindow.getSendTime(seqN);

    Volt * auxVolt = slidingWindow.dupVolt(seqN);

    if(auxVolt != NULL) {
		simtime_t ack_time = simTime() - auxVolt->getCreationTime();
		ackTime.record(ack_time);
		simtime_t rtt_time = simTime() - slidingWindow.getSendTime(seqN);
		rtt.record(rtt_time);
	}

    if (auxVolt != NULL && !auxVolt->getRetFlag()) {
		// Update stimated RTT
		double newRtt = (simTime().dbl() - sendTime);
		rttManager.updateEstimation(newRtt);
	}

    // Update SW when is ACK
    while (0 < slidingWindow.getAck(slidingWindow.getBaseWindow())) {
        // Get current base of Sliding Window
        int currentBaseOfSW = slidingWindow.getBaseWindow();

        // Remove packet
        Volt * storedPkt = slidingWindow.popVolt(currentBaseOfSW);
        delete(storedPkt);

        // Update SW
        slidingWindow.setBaseWindow(
            (currentBaseOfSW + 1) % 1000);
    }


    // Remove used packet and aux packet
    delete(auxVolt);
	delete(volt);
}

void TransportSender::handlePacketLoss(int seqN){
    // Cancel current timeout
	EventTimeout * timeout = renoManager.popTimeoutMsg(seqN);

    if(timeout != NULL){
		cancelEvent(timeout);
		delete(timeout);
	}

    // Add lost packet to retransmission queue
    retransmissionQueue.push_back(seqN);
	rttManager.updateTimeoutRTo();

	scheduleServiceIfIdle();

    // Update congestion window (CW) - Reno
    int newCWSize = renoManager.getSize() / 2;
	renoManager.setSize(newCWSize);
	renoManager.setSlowStart(false);
}

/**
 * Starts the next packet transmission if allowed by flow control.
*/
void TransportSender::handleStartNextTransmission() {
    std::cout << "TrSender :: handleStartNextTransmission()\n";
    Volt * voltToSend = NULL;

    if(!retransmissionQueue.empty()) {
        int retSeqN = retransmissionQueue.front();
		retransmissionQueue.pop_front();

		voltToSend = slidingWindow.dupVolt(retSeqN);
		voltToSend->setRetFlag(true);

        // Console debug
		std::cout << "TrSender :: Sending Volt from retransmission Queue\n";

        // Update metrics
		packetRetransSen.collect(1);
    } else {
        voltToSend = (Volt *) buffer.pop();

        Volt * voltAux = voltToSend->dup();

        slidingWindow.addVolt(voltAux);
        slidingWindow.addSendTime(voltToSend->getSeqNumber(), simTime().dbl());
    }

    bufferSizeStdSen.collect(buffer.getLength());
	bufferSizeSen.record(buffer.getLength());

    // Send packet
    send(voltToSend, "subnetwork$o");

    simtime_t serviceTime = voltToSend->getDuration();
	scheduleAt(simTime() + serviceTime, endServiceEvent);

    // Add new EventTimeout
    EventTimeout * timeout = new EventTimeout("timeout", EVENT_TIMEOUT_KIND);

    timeout->setSeqN(voltToSend->getSeqNumber());
    timeout->setPacketSize(voltToSend->getByteLength());

    scheduleAt(simTime() + rttManager.getCurrentRTo(), timeout);
    renoManager.addTimeoutMsg(timeout);
    std::cout << "TrSender :: END handleStartNextTransmission()\n";
}

void TransportSender::scheduleServiceIfIdle() {
	// If we are not sending a message right now
	if (!endServiceEvent->isScheduled()) {
		// Schedule packet shipping
		scheduleAt(simTime() + 0, endServiceEvent);
	}
}

#endif /* TRANSPORTSENDER */
