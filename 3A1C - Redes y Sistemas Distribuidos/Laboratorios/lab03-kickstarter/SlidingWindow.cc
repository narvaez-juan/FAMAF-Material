#ifndef SLIDINGWINDOW
#define SLIDINGWINDOW

#include <string.h>
#include <omnetpp.h>
#include "SlidingWindow.h"

using namespace omnetpp;

typedef std::map<int,packetMetadata>::iterator windowIterator;

SlidingWindow::SlidingWindow() {}

SlidingWindow::~SlidingWindow() {}

/* Returns the number of ACKs that Volt has */
int SlidingWindow::getAck(int seqN) {
    windowIterator pairIterator = slidingWindow.find(seqN);

    if (pairIterator == slidingWindow.end()) {
        // It does not exist in the dictionary
        return -1;
    }

    return pairIterator->second->ackCounter;
}

/* If there is a volt with that sequence, increment the ACK counter by one */
void SlidingWindow::addAck(int seqN) {
    windowIterator iterator = slidingWindow.find(seqN);

    if (iterator != slidingWindow.end()) {
        //iterator->second->ackCounter++;  // FIXME

        packetMetadata pair = iterator->second;
		(pair->ackCounter)++;

        std::cout << "SW :: ackCounter[" << seqN << "]++ " << pair->ackCounter << "\n";

        slidingWindow[seqN] = pair;
        //slidingWindow[seqN] = iterator->second;  // FIXME
    }
}

/* Add the volt to the window */
void SlidingWindow::addVolt(Volt* volt) {
    int seqN = volt->getSeqNumber();

    packetMetadata metadata = new _packetMetadata();
    metadata->volt = volt;
    metadata->ackCounter = 0;
    metadata->sendTime = 0.0;
    metadata->retransmitted = false;

    slidingWindow[seqN] = metadata;
    bytesInFlight += volt->getByteLength();
}

/*
* Returns the window's volt by removing its reserved space
* Returns NULL if no volt is found with that seqN
*/
Volt* SlidingWindow::popVolt(int seqN) {
    Volt * volt = NULL;

    windowIterator iterator = slidingWindow.find(seqN);

    if (iterator != slidingWindow.end()) {
        volt = iterator->second->volt;

        delete(iterator->second);
        slidingWindow.erase(iterator);

        bytesInFlight -= volt->getByteLength();
    } else {
		std::cout << "SW :: WARNING :: popVolt could not find Volt " << seqN << "\n";
	};

    return volt;
}

/*
* Returns a copy of the Volt. The user must delete it.
* Returns NULL if no volt with that seqN is found.
*/
Volt* SlidingWindow::dupVolt(int seqN) {
    Volt * volt = NULL;

    windowIterator iterator = slidingWindow.find(seqN);

    if (iterator != slidingWindow.end() && iterator->second->volt != NULL) {
        volt = iterator->second->volt->dup();
    }

    return volt;
}

/* Returns if the volt is in the SW */
bool SlidingWindow::isVoltInWindow(int seqN) {
    return slidingWindow.find(seqN) != slidingWindow.end();
}

/* Returns the Volt shipping time */
double SlidingWindow::getSendTime(int seqN) {
    windowIterator iterator = slidingWindow.find(seqN);

    if (iterator != slidingWindow.end()) {
        return iterator->second->sendTime;
    }

    return -1;
}

/* Add Volt shipping time */
void SlidingWindow::addSendTime(int seqN, double time) {
    windowIterator iterator = slidingWindow.find(seqN);

    if (iterator != slidingWindow.end()) {
        iterator->second->sendTime = time;
        slidingWindow[seqN] = iterator->second;
    }
}

/* Returns the seqN of the base of the SW */
int SlidingWindow::getBaseWindow() {
    return baseWindow;
}

/* Set the seqN of the SW base */
void SlidingWindow::setBaseWindow(int base) {
    baseWindow = base;
}

/* Returns the number of bytes that are being sent */
int SlidingWindow::amountBytesInFlight() {
    return bytesInFlight;
}

#endif /* SLIDINGWINDOW */
