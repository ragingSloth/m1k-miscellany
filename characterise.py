import usb
import time
import numpy as np
import pprint
import pickle
from libpysmu import smu

device = smu()
d = usb.core.find(idVendor=0x064b,idProduct=0x784c)
uid = device.devices[0][0]

saveData = {'uid': uid}
for name,chan in device.chans.items():
	svmiPoints = np.linspace(0, 5, 50)
	data = []
	for vval in svmiPoints:
		chan.set_mode('v')
		chan.constant(vval)
		newData = chan.get_samples(50)
		data += [[np.mean([x[0] for x in newData]), np.mean([x[1] for x in newData])]]
	
	data = np.array(data).T
	currentOffset = np.mean(data[1])
	saveData['current offset '+name] = currentOffset
	chan.set_mode('d')
	if name == 'A':
		d.ctrl_transfer(0x40,0x50,32,0,0)
	if name == 'B':
		d.ctrl_transfer(0x40,0x50,37,0,0)
	newData = chan.get_samples(50)
	voltageOffset = np.mean([x[0] for x in newData])
	saveData['voltage offset '+name] = voltageOffset
	simvPoints = np.linspace(-0.04, 0.04, 50)
	data = []
	for ival in simvPoints:
		chan.set_mode('i')
		chan.constant(ival)
		newData = chan.get_samples(50)
		data += [[ival, np.mean([x[0] for x in newData]), np.mean([x[1] for x in newData])]]
	data = np.array(data).T
	saveData['current source offset '+name] = data
	if name == 'A':
		d.ctrl_transfer(0x40,0x51,32,0,0)
	if name == 'B':
		d.ctrl_transfer(0x40,0x51,37,0,0)

pprint.pprint(saveData)
pickle.dump(saveData, open(uid+'+'+str(int(time.time()))+'.p', 'w'))
