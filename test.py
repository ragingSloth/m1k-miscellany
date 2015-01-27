import subprocess
import usb
import time

def bootload():
    dev = usb.core.find(idVendor=0x064b, idProduct=0x784c)
    if not dev:
         dev = usb.core.find(idVendor=0x0456, idProduct=0x784c)
    if dev:
         try:
             dev.ctrl_transfer(0x40|0x80, 0xBB, 0, 0, 1)
             return False
         except:
             return True

pio = lambda x: subprocess.Popen(["pio", "-m", x])

while True:
   while not usb.core.find(idProduct=0x6124, idVendor=0x03eb):
      time.sleep(1)
      bootload()
   flash_pipe = subprocess.Popen(["python", "sam-ba.py"])
   flash_pipe.wait()
   pio("PB9*1")
   time.sleep(1)
   pio("PB9*1")
   time.sleep(1)
   if usb.core.find(idVendor=0x064b,idProduct=0x784c):
       char_pipe = subprocess.Popen(["python", "characterise.py"])
       char_pipe.wait()
       print 'characterisation complete'
       for i in range(4):
   	       pio("PH24*1")
   	       time.sleep(1)
       pio("PB9*1")
       time.sleep(10)
       pio("PB9*1")
