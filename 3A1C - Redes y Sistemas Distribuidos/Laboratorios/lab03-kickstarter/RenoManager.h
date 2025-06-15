#ifndef __RENOMANAGER_H
#define __RENOMANAGER_H

#include <omnetpp.h>
#include "EventTimeout_m.h"

#define EVENT_TIMEOUT_KIND 1

class RenoManager {
private:
    int maxSize;
    int size;
    int msgSendingAmount;
    bool isSlowStartStage = true;
    std::map<int, EventTimeout*> window;
public:
    RenoManager();
    virtual ~RenoManager();

    // Own methods
    int getMaxSize();
    int getSize();
    int getAvailableWin();
    void setSize(int newSize);
    void addTimeoutMsg(EventTimeout * msg);
    EventTimeout * popTimeoutMsg(int seqN);
    bool getSlowStart();
    void setSlowStart(bool state);
protected:
};

#endif // ifndef __RENOMANAGER_H
