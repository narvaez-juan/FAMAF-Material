#ifndef __RTTMANAGER_H
#define __RTTMANAGER_H

#include <omnetpp.h>
#include "Volt_m.h"

class RTTManager {
private:
	double stdDesviation;
	double rtt;
    double rto;
    bool isFirstAckReceived;
    void updateSmoothRTT(double rtMeasurement);
public:
	RTTManager();
    virtual ~RTTManager();

    /* RTo = Retransmission Timeout */
	double getCurrentRTo();

    void updateTimeoutRTo();

    /* rtMeasurement = Round Trip Measurement */
    void updateEstimation(double rtMeasurement);

    double getCurrentRTT();
protected:
	//
};

#endif // ifndef __RTTMANAGER_H

