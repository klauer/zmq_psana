#!/usr/bin/env python3
# source /reg/g/pcds/pyps/conda/py36env.sh
from fakepsana import *
import time
import matplotlib.pyplot as plt

ds = DataSource()
d = Detector("DsaCsPad")
d2 = Detector("FEEGasDetEnergy")
for e in ds.events():
    evtId = e.get(EventId)
    print("Got data at %d.%09d (%d 0x%x)" % (evtId.time()[0], evtId.time()[1], evtId.fiducials(), evtId.fiducials()))
    data = d.calib(e)
    print(data.shape)
    enrc = d2.get(e)
    plt.imshow(data[0])
    plt.pause(1)
    print("11 = %g, 12 = %g" % (enrc.f_11_ENRC(), enrc.f_12_ENRC()))
    print("")
