//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

#ifndef __PI_FLOODING_H_
#define __PI_FLOODING_H_

#include <omnetpp.h>
#include "veins/modules/application/ieee80211p/BaseWaveApplLayer.h"

/**
 * TODO - Generated class
 */
class Flooding: public BaseWaveApplLayer {
public:
    enum WaveApplMessageKinds {
        SEND_WSM_EVT = 10
    };

    virtual void initialize(int stage);
    virtual void finish();
protected:
    virtual void onBSM(BasicSafetyMessage* bsm);
    virtual void onWSM(WaveShortMessage* wsm);
    virtual void onWSA(WaveServiceAdvertisment* wsa);

    virtual void handleSelfMsg(cMessage* msg);
    virtual void handlePositionUpdate(cObject* obj);

protected:
    u_int32_t numMsgs;
    u_int32_t msgsCounter;
    bool isSource; //is this node source?
    simtime_t wsmInterval;
    simtime_t stopTrafficTime;
    bool trafficStopped;
    bool isFirstMessage;
    bool reached;
    cMessage* sendWSMEvt;
};

#endif
