#ifndef RENOMANAGER
#define RENOMANAGER

#include <omnetpp.h>
#include "EventTimeout_m.h"
#include "RenoManager.h"

using namespace omnetpp;

typedef std::map<int, EventTimeout*>::iterator cwIterator;

RenoManager::RenoManager() {
	maxSize = 2147483640;
	size = 0;
	msgSendingAmount = 0;
}

RenoManager::~RenoManager() {
}


// Implementacion de las funciones

// Devuelve tamaño máximo de ventana de congestión
int RenoManager::getMaxSize() {
    return this->maxSize;
}

// Devuelve tamaño actual de ventana de congestión
int RenoManager::getSize() {
    return this->size;
}

// Devuelve el tamaño de la ventana de congestión disponible
int RenoManager::getAvailableWin() {
    int availableWindow = this->size - this->msgSendingAmount;
    availableWindow = std::max(0, availableWindow);
    return availableWindow;
}

// Modifica el tamaño de la ventana de congestión
void RenoManager::setSize(int newSize) {
    if (newSize <= this->maxSize) {
        this->size = newSize;
    }
}

// Agrega un evento que representa que un mensaje fue enviado y está en la sub red
void RenoManager::addTimeoutMsg(EventTimeout * msg) {
    if (msg == NULL) {
        // null message
    } else if (getAvailableWin() >= msg->getPacketSize()) {
        int seqNum = msg->getSeqN();
        this->window[seqNum] = msg;
        this->msgSendingAmount += msg->getPacketSize();
    } else {
        // windows no space for timeout
    }
}

// Elimina un mensaje de la ventana de congestión, la cual devuelve
EventTimeout * RenoManager::popTimeoutMsg(int seqN) {
    cwIterator timeoutIterator = window.find(seqN);
	if (timeoutIterator == window.end()) {
        // warning trying to pop when window has no event
		return NULL;
	}
	EventTimeout * event = timeoutIterator->second;
	msgSendingAmount -= event->getPacketSize();
	window.erase(timeoutIterator);
	return event;
}

// Devuelve si el estado de la ventana de congestión está en la etapa de arranque lento
bool RenoManager::getSlowStart() {
    return this->isSlowStartStage;
}

// Modifica si la ventana de econgestion esta en estado de arranque lento
void RenoManager::setSlowStart(bool state) {
    this->isSlowStartStage = state;
}

#endif /* RENOMANAGER */
