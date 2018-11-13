from fakepsana import *
import time

ds = DataSource()
d = Detector("cspad")
d2 = Detector("FEEGasDetEnergy")
for e in ds.events():
    evtId = e.get(EventId)
    print("Got data at %d.%09d (%d 0x%x)" % (evtId.time()[0], evtId.time()[1], evtId.fiducials(), evtId.fiducials()))
    data = d.calib(e)
    print(data.shape)
    enrc = d2.get(e)
    print("11 = %g, 12 = %g" % (enrc.f_11_ENRC(), enrc.f_12_ENRC()))
    print("")
