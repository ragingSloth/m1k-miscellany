import subprocess
import usb
import time

def bootload():
    dev = usb.core.find(idVendor=0x064b, idProduct=0x784c)
    if dev:
         try:
             dev.ctrl_transfer(0x40|0x80, 0xBB, 0, 0, 1)
             return False
         except:
             return True

pio = lambda x: subprocess.Popen(["pio", "-m", x])


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
       char_pipe = subprocess.Popen(["python", "characterise.py"])
       char_pipe.wait()
       for i in range(4):
   	       pio("PH24*1")
   	       time.sleep(1)

