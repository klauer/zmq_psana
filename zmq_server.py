#!/usr/bin/env python
#source /reg/g/psdm/etc/psconda.sh

import zmq
from psana import *
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:25000")

## Set the DataSource here!!
#ds = DataSource()
ds = DataSource('exp=xpptut15:run=54:smd')

all_alias = {}
for (a, b, c) in DetNames():    # (Official, DAQ, User) tuples.
    all_alias[a] = a
    if b != "":
        all_alias[b] = a
    if c != "":
        all_alias[c] = a

feedet = Detector("FEEGasDetEnergy")
## ADD additional special type detectors here!!

imgs = []

imgs.append((Detector("cspad"), "calib"))
## ADD/MODIFY detectors here!!

for evt in ds.events():
    dl = []
    np = []
    for (d, access) in imgs:
        ## ADD additional access methods for detectors here!! (Default: only calib supported.)
        if access == 'calib':
            data = d.calib(evt)
        else:
            raise Exception("Unsupported access %s." % access)
        dl.append(data)
        np.append((str(d.name), access, str(data.dtype), data.shape))

    enrc  = feedet.get(evt)
    evtId = evt.get(EventId)
    ## Access data for additional special detectors here!!

    md = dict(
        evtId = [evtId.fiducials(), evtId.run(), evtId.ticks(), evtId.time(), evtId.vector()],
        enrc  = [enrc.TypeId, enrc.Version,
                 enrc.f_11_ENRC(), enrc.f_12_ENRC(), enrc.f_21_ENRC(), 
                 enrc.f_22_ENRC(), enrc.f_63_ENRC(), enrc.f_64_ENRC()],
        ## Pass in information for additional special detectors here!!
        alias = all_alias,
        npdata = np
    )
    socket.send_pyobj(md, flags=zmq.SNDMORE)
    for data in dl:
        socket.send(data, flags=zmq.SNDMORE)
    socket.send("")
    print "Sent %d.%09d (%d 0x%x)" % (md['evtId'][3][0], md['evtId'][3][1],
                                      md['evtId'][0], md['evtId'][0])
