import atexit
from operator import add

import pysmu


class smu(object):
    def __init__(self):
        atexit.register(pysmu.cleanup)
        pysmu.setup()
        self.load_chans()


    def load_chans(self):
        self.devices = pysmu.get_dev_info()
        self.serials = {i:v[0] for i, v in enumerate(self.devices)}
        self.devices = [x[1] for x in self.devices]

        names = (chr(x) for x in xrange(65,91))
        self.chans = {names.next(): (i, v) for i, d in enumerate(self.devices) for k, v in d.items()}
        self.chans = {k: channel(k, *v) for k, v in self.chans.items()}
        self.devices = {i:(self.serials[i], v) for i, v in enumerate(self.devices)}

    def ctrl_transfer(self, device, bm_request_type, b_request, wValue, wIndex, data, wLength, timeout):
	data = str(data)
        return pysmu.ctrl_transfer(device, bm_request_type, b_request, wValue, wIndex, data, wLength, timeout)

    def __repr__(self):
        return 'Devices: '+str(self.devices)



class channel(object):
    def __init__(self, chan, dev, signals):
        self.chan = ord(chan) - 65
        self.dev = dev
        self.signals = {v: i for i, v in enumerate(signals)}


    def set_mode(self, mode):
        if mode == 'v' or mode == 'V':
            pysmu.set_mode(self.dev, self.chan, 1)
            self.mode = 1
        elif mode == 'i' or mode == 'I':
            pysmu.set_mode(self.dev, self.chan, 2)
            self.mode = 2
        elif mode == 'd' or mode =='D':
            pysmu.set_mode(self.dev, self.chan, 0)
            self.mode = 0
        else:
            raise Exception('invalid mode')

    def arbitrary(self, *args, **kwargs):
        repeat = 0
        if 'repeat' in map(str.lower, kwargs.keys()):
            repeat = 1
        wave = map(float, reduce(add, [[s]*100*n for s, n in args]))
        return pysmu.set_output_buffer(wave, self.dev, self.chan, self.mode, repeat)

    def get_samples(self, n_samples):
        return pysmu.get_inputs(self.dev, self.chan, n_samples)

    def constant(self, val):
        return pysmu.set_output_constant(self.dev, self.chan, self.mode, val)
    def square(self, midpoint, peak, period, phase, duty_cycle):
        return pysmu.set_output_wave(self.dev, self.chan, self.mode, 1, midpoint, peak, period, phase, duty_cycle)
    def sawtooth(self, midpoint, peak, period, phase):
        return pysmu.set_output_wave(self.dev, self.chan, self.mode, 2, midpoint, peak, period, phase, 42)
    def sine(self, midpoint, peak, period, phase):
        return pysmu.set_output_wave(self.dev, self.chan, self.mode, 3, midpoint, peak, period, phase, 42)
    def triangle(self, midpoint, peak, period, phase):
        return pysmu.set_output_wave(self.dev, self.chan, self.mode, 4, midpoint, peak, period, phase, 42)

    def __repr__(self):
        return 'Dev: '+str(self.dev)+'\nChan: '+str(self.chan)+'\nSignals: '+str(self.signals)

if __name__ == '__main__':
    x = smu()
    print x
    print x.devices
    A = x.chans['A']
    A.set_mode('v')
    A.constant(3)
    #A.arbitrary((5, 400), (2.5, 400))
    #print A.sine(1, 3, 5, 0)
    #print A.square(0, 3, 10, 0, .5)
    #print A.triangle(2,3,10,0)
    print A.get_samples(1000)
