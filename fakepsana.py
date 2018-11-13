#
# A make-believe version of psana for python3
#

import zmq
import numpy

_ds = None

def DataSource(ds=None):
    global _ds
    _ds = _DataSource(ds)
    return _ds

def Detector(name):
    d = _Detector(name)
    return d

class _DataSource(object):
    def __init__(self, ds):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt(zmq.SUBSCRIBE, b"")
        self.socket.connect("tcp://localhost:25000")

    def events(self):
        return self

    def __iter__(self):
        return self

    def __next__(self):
        return Event(self)

class Event(object):
    def __init__(self, ds):
        md = ds.socket.recv_pyobj()
        self._alias = md['alias']
        self._data = {}
        self._access = {}
        for np in md['npdata']:
            data = ds.socket.recv()
            data = numpy.frombuffer(data, dtype=np[2])
            data = data.reshape(np[3])
            self._data[np[0]] = data
            self._access[np[0]] = np[1]
        data = ds.socket.recv() # Final ""!
        ## Special detectors processing.
        self._evtId = EventId(md['evtId'])
        self._enrc  = BldDataFEEGasDetEnergyV1(md['enrc'])
        self._access['FEEGasDetEnergy'] = 'get'
        self._data['FEEGasDetEnergy'] = self._enrc
        ## Add data/access for additional special type detectors here!!
    
    def get(self, tp):
        if tp == EventId:
            return self._evtId
        else:
            raise Exception("Event.get failed!")

    def _do_access(self, access, name):
        name = self._alias[name]
        try:
            if self._access[name] == access:
                return self._data[name]
        except:
            raise Exception("Detector %s does not support '%s'" % (name, access))

class _Detector(object):
    def __init__(self, name):
        self.name = name

    def get(self, evt):
        return evt._do_access("get", self.name)

    def calib(self, evt):
        return evt._do_access("calib", self.name)

    ## Add extra access methods for detectors here!

class EventId(object):
    def __init__(self, vec):
        self._vec = vec

    def fiducials(self):
        return self._vec[0]

    def run(self):
        return self._vec[1]

    def ticks(self):
        return self._vec[2]

    def time(self):
        return self._vec[3]

    def vector(self):
        return self._vec[4]

class BldDataFEEGasDetEnergyV1(object):
    def __init__(self, vec):
        self.TypeId = vec[0]
        self.Version = vec[1]
        self._vec = vec

    def f_11_ENRC(self):
        return self._vec[2]

    def f_12_ENRC(self):
        return self._vec[3]

    def f_21_ENRC(self):
        return self._vec[4]

    def f_22_ENRC(self):
        return self._vec[5]

    def f_63_ENRC(self):
        return self._vec[6]

    def f_64_ENRC(self):
        return self._vec[7]

"""
ebeamDet = Detector('EBeam')
for nevent,evt in enumerate(ds.events()):
    ebeam = ebeamDet.get(evt)
    if ebeam is None: continue

det = Detector('cspad')
for nevent,evt in enumerate(ds.events()):
    # includes pedestal subtraction, common-mode correction, bad-pixel
    # suppresion, and returns an "unassembled" 3D array of cspad panels
    calib_array = det.calib(evt)
    # this is the same as the above, but also uses geometry to
    # create an "assembled" 2D image (including "fake pixels" in gaps)
    img = det.image(evt)
    break
"""
