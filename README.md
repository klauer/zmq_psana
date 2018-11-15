Used in jet tracking testing at CXI in late 2018.

From mcbrowne:

```
I give unto you ~mcbrowne/zmq.  In this directory, you will find:
    * zmq_server.py - A python2 psana script that sets up a ZMQ socket at port 25000.
    * fakepsana.py - Something that pretends to be psana in python3.
    * test.py - A python3 test script that uses fakepsana.py

This should be extendable if we need to add additional detectors.  Right now it supports:
event.get(EventId) to get the timing information.

* detector("cspad").calib(event) to get the calibrated data for a cspad/area detector image.
* detector("FEEGasDetEnergy").get(event) to get the FEE gas detector energy object.

By default, zmq_server.py gets data from some random XPP experiment, but we can
easily change the DataSource argument.
```
