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

#include "Flooding.h"

Define_Module(Flooding);

void Flooding::initialize(int stage) {
    // TODO - Generated method body
    BaseWaveApplLayer::initialize(stage);
    if (stage == 0) {
        //Initializing members and pointers of your application goes here
        sendWSMEvt = new cMessage("wsm evt", SEND_WSM_EVT);
        wsmInterval = par("wsmInterval").doubleValue();
        numMsgs = par("numMsgs").longValue();
        isSource = par("isSource").boolValue();
        stopTrafficTime = par("stopTrafficTime").doubleValue();
        trafficStopped = false;
        isFirstMessage = true;
        reached = false;
        msgsCounter = 0;
        if(isSource){
            scheduleAt(computeAsynchronousSendingTime(simTime() + wsmInterval,type_SCH), sendWSMEvt);
        }

    } else if (stage == 1) {
        //Initializing members that require initialized other modules goes here

    }
}
void Flooding::finish() {
    BaseWaveApplLayer::finish();
    //statistics recording goes here

}

void Flooding::onBSM(BasicSafetyMessage* bsm) {
    //Your application has received a beacon message from another car or RSU
    //code for handling the message goes here

}

void Flooding::onWSM(WaveShortMessage* wsm) {
    //Your application has received a data message from another car or RSU
    //code for handling the message goes here, see TraciDemo11p.cc for examples
    if(!reached){
        findHost()->getDisplayString().updateWith("r=16,green");
        reached = true;
        sendDown(wsm->dup());
    }

    /*if(!isSource){
        msgsCounter++;
    }*/
}

void Flooding::onWSA(WaveServiceAdvertisment* wsa) {
    //Your application has received a service advertisement from another car or RSU
    //code for handling the message goes here, see TraciDemo11p.cc for examples

}

void Flooding::handleSelfMsg(cMessage* msg) {
    switch (msg->getKind()) {
        case SEND_WSM_EVT: {
            if ((msgsCounter < numMsgs) and isSource) {
                WaveShortMessage* wsm = new WaveShortMessage();
                populateWSM(wsm);
                sendDown(wsm);
                if(isFirstMessage){
                    findHost()->getDisplayString().updateWith("r=16,green");
                    reached = true;
                    isFirstMessage = false;
                }
                msgsCounter++;    //Increment number of messages sent
                scheduleAt(simTime() + wsmInterval, sendWSMEvt);
                break;
            }

        }
        default: {
            if (msg)
                DBG_APP << "APP: Error: Got Self Message of unknown kind! Name: "
                               << msg->getName() << endl;
            break;
    }
    }
    //BaseWaveApplLayer::handleSelfMsg(msg);
    //this method is for self messages (mostly timers)
    //it is important to call the BaseWaveApplLayer function for BSM and WSM transmission

}

void Flooding::handlePositionUpdate(cObject* obj) {
    BaseWaveApplLayer::handlePositionUpdate(obj);

    //Stopping all vehicles
    /*if(simTime() == stopTrafficTime){

        traciVehicle->setSpeed(0.0);
        trafficStopped = true;
    }

    if(trafficStopped){
        //Only source node will schedule the event to begin the PI
        if(isSource and isFirstMessage){
            findHost()->getDisplayString().updateWith("r=16,green");
            scheduleAt(computeAsynchronousSendingTime(simTime() + wsmInterval,type_SCH), sendWSMEvt);
            isFirstMessage = false;
            reached = true;
        }
    }

    if(msgsCounter > numMsgs){
        traciVehicle->setSpeed(3.0);
    }*/

    //the vehicle has moved. Code that reacts to new positions goes here.
    //member variables such as currentPosition and currentSpeed are updated in the parent class

}

