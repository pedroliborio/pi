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

package com.liborio.pi.Flooding;
import org.car2x.veins.modules.application.ieee80211p.BaseWaveApplLayer;
//
// TODO auto-generated module
//
simple Flooding extends BaseWaveApplLayer
{
    @class(Flooding);//This is needed to reference where the class behaviour will be builded
    double wsmInterval = default(1s) @unit(s);
    int numMsgs = default(100);
    bool isSource = default(false);
    double stopTrafficTime @unit(s);
}
