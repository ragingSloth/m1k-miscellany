import subprocess
import usb
import time
from libpysmu import smu

def bootload():
   dev = usb.core.find(idVendor=0x064b, idProduct=0x784c)
   if dev:
        try:
   	    dev.ctrl_transfer(0x40|0x80, 0xBB, 0, 0, 1)
            return False
        except:
            return True
   

pio = lambda x: subprocess.Popen(["pio", "-m", x])

#usb.core.find(idProduct=0x6124, idVendor=0x03eb)

bootload()
while True:
   while not usb.core.find(idProduct=0x6124, idVendor=0x03eb):
      time.sleep(1)
   # wait for user input, remove this eventually
   # should check for retval of 1
   bootload()
   time.sleep(1)
   flash_pipe = subprocess.Popen(["python", "sam-ba.py"])
   flash_pipe.wait()
   pio("PB9*1")
   time.sleep(1)
   pio("PB9*1")
   time.sleep(1)
   if usb.core.find(idVendor=0x064b,idProduct=0x784c):
   	for i in range(4):
   	    pio("PH24*1")
   	    time.sleep(1)
	device = smu()
	d = usb.core.find(idVendor=0x064b,idProduct=0x784c)

	A = device.chans['A']
	A.set_mode('v')
	A.constant(1)
	data = [reduce(lambda x, y: (x[0]+y[0], x[1]+y[1]), A.get_samples(500))]
	A.set_mode('v')
	A.constant(2)
	data.append(reduce(lambda x, y: (x[0]+y[0], x[1]+y[1]), A.get_samples(500)))
	A.set_mode('v')
	A.constant(3)
	data.append(reduce(lambda x, y: (x[0]+y[0], x[1]+y[1]), A.get_samples(500)))
	A.set_mode('v')
	A.constant(4)
	data.append(reduce(lambda x, y: (x[0]+y[0], x[1]+y[1]), A.get_samples(500)))
	A.set_mode('v')
	A.constant(5)
	data.append(reduce(lambda x, y: (x[0]+y[0], x[1]+y[1]), A.get_samples(500)))
	print map(lambda x: (x[0]/500.0, x[1]/500.0), data)


	d.ctrl_transfer(0x40,0x50,32,0,1)

	A.set_mode('i')
	A.constant(-.1)
	data = [reduce(lambda x, y: (x[0]+y[0], x[1]+y[1]), A.get_samples(500))]
	A.set_mode('i')
	A.constant(-.05)
	data.append(reduce(lambda x, y: (x[0]+y[0], x[1]+y[1]), A.get_samples(500)))
	A.set_mode('i')
	A.constant(0)
	data.append(reduce(lambda x, y: (x[0]+y[0], x[1]+y[1]), A.get_samples(500)))
	A.set_mode('i')
	A.constant(.05)
	data.append(reduce(lambda x, y: (x[0]+y[0], x[1]+y[1]), A.get_samples(500)))
	A.set_mode('i')
	A.constant(.1)
	data.append(reduce(lambda x, y: (x[0]+y[0], x[1]+y[1]), A.get_samples(500)))
	print map(lambda x: (x[0]/500.0, x[1]/500.0), data)

	d.ctrl_transfer(0x40,0x51,32,0,1)

