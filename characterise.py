import usb
import time
import numpy as np
from libpysmu import smu

device = smu()
d = usb.core.find(idVendor=0x064b,idProduct=0x784c)
print device.devices[0][0]
A = device.chans['A']

svmiPoints = np.linspace(0, 5, 500)
data = []
for vval in svmiPoints:
	A.set_mode('v')
	A.constant(vval)
	newData = A.get_samples(500)
	data += [[np.mean([x[0] for x in newData]), np.mean([x[1] for x in newData])]]

data = np.array(data).T
currentOffset = np.mean(data[1])
print currentOffset

A.set_mode('d')
d.ctrl_transfer(0x40,0x50,32,0,0)
newData = A.get_samples(500)
voltageOffset = np.mean([x[0] for x in newData])
print voltageOffset

simvPoints = np.linspace(-0.04, 0.04, 500)

data = []
for ival in simvPoints:
	A.set_mode('i')
	A.constant(ival)
	newData = A.get_samples(500)
	data += [[np.mean([x[0] for x in newData]), np.mean([x[1] for x in newData])]]

data = np.array(data).T

d.ctrl_transfer(0x40,0x51,32,0,0)

from pylab import *
plot(simvPoints, data[1]-simvPoints, '.')
show()
