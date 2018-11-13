#!/usr/bin/env python3
#up python3-dev
#setenv PYTHONPATH /reg/g/pcds/pkg_mgr/release/python3-dev/x86_64-rhel7-gcc48-opt/python:/reg/neh/home/mcbrowne/zmq/lib/python3.6/site-packages

import zmq
import numpy

context = zmq.Context()
socket = context.socket(zmq.SUB)
#socket.setsockopt(zmq.SUBSCRIBE, "")
socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.connect("tcp://localhost:25000")

while True:
    #md = socket.recv_json()
    md = socket.recv_pyobj()
    msg = socket.recv()
    print(md)
    #buf = buffer(msg)
    #result = numpy.frombuffer(buf, dtype=md['dtype'])
    result = numpy.frombuffer(msg, dtype=md['dtype'])
    result = result.reshape(md['shape'])
    print("Got %d.%09d (%d 0x%x)" % (md['secs'], md['nsec'], md['fid'], md['fid']))
    print(result)
