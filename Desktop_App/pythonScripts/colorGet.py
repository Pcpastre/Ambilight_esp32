from operator import gt
from PIL import ImageGrab
import time
import numpy as np
from flask import Flask, request
from threading import *
import requests
import serial


THREADS = []

app = Flask(__name__) 


print(hex)

class colorGet(Thread):
    def __init__(self, ip):
        try:
            Thread.__init__(self)

            self.ipDisp = ip
            self.alive = True
            self.SEND_DATA = []

        except:
            print("Error in AudioBars!")

    def run(self):
        while (self.alive):
                    try:
                        ipD = '192.168.0.162'
                        rT = 0
                        gT = 0
                        bT = 0
                        count = 0;
                        time.process_time()
                        image = ImageGrab.grab()
                        xI, yI = image.size
                        print(xI , yI)
                        for y in range(0, yI, 10):
                            for x in range(0, xI, 10):
                                r,g,b = image.getpixel((x, y))
                                rT = rT + r
                                gT = gT + g
                                bT = bT + b
                                count = count + 1
                        print(time.process_time())
                        print(int(rT/count), int(gT/count), int(bT/count))
                        rS = str(int(rT/count))
                        gS = str(int(gT/count))
                        bS = str(int(bT/count))
                        req = requests.get('http://'+ ipD +'/colorSend?R=' +rS+ '&G=' +gS+ '&B=' + bS)
                        req.status_code
                        
                    except:
                        # Sometimes the APP stuck and this exception happens in a loop
                        print("Error in AudioBars")
                        self.alive  = False




@app.route('/Start', methods=["GET"])
def Start():
    
    ipDisp = request.args.get('ipDisp')

    m = colorGetM(ipDisp)
    m.start()
    THREADS.append(m)
    m = colorGet(ipDisp)
    m.start()
    THREADS.append(m)
    response = "Start"
    return response

@app.route('/Stop', methods=["GET"])
def Stop():
    
    # Just an empty JSON
   

    print("Stoping the mic...")

    # Stopping the Microphone
    for t in THREADS:
        t.alive = False

    response = "Stop"
    return response

@app.route('/StartM', methods=["GET"])
def StartM():
    
    ipDisp = request.args.get('ipDisp')
    for t in THREADS:
        t.alive = False
    t = colorGetM(ipDisp)
    t.start()
    THREADS.append(t)
    response = "Start"
    return response


colorsM = []

class colorGetM(Thread):
    def __init__(self, ip):
        try:
            Thread.__init__(self)

            self.ipDisp = ip
            self.alive = True
            self.SEND_DATA = []

        except:
            print("Error in AudioBars!")

    def run(self):
        while (self.alive):
            ipD = "192.168.0.162"
            time.process_time()
            image = ImageGrab.grab()
            xI, yI = image.size
            print(xI , yI)
            rT = 0
            gT = 0
            bT = 0
            crxs = 0
            cgxs = 0
            cbxs = 0
            count = 0
            count1 = 0
            finalString = "colorSend2"
            for y in range(899, 675, -5):
                for x in range(0, 360, 5):
                    r,g,b = image.getpixel((x, y))
                    rT = rT + r
                    gT = gT + g
                    bT = bT + b
                    count = count + 1

            
            rx = hex(int(rT/count))
            gx = hex(int(gT/count))
            bx = hex(int(bT/count))
        
            rxs = rx.split("x", 2)
            bxs = bx.split("x", 2)
            gxs = gx.split("x", 2)
            
            if(len(rxs[1]) == 1):
                crxs = ord(rxs[1])
                if((crxs >= 48 and  crxs <= 57) or (crxs >= 97 and  crxs <= 102)):
                    rxs[1] = "0" + rxs[1]
                    
            if(len(gxs[1]) == 1):
                cgxs = ord(gxs[1])
                if((cgxs >= 48 and  cgxs <= 57) or (cgxs >= 97 and  cgxs <= 102)):
                    gxs[1] = "0" + gxs[1]

            if(len(bxs[1]) == 1):
                cbxs = ord(bxs[1])
                if((cbxs >= 48 and  cbxs <= 57) or (cbxs >= 97 and  cbxs <= 102)):
                    bxs[1] = "0" + bxs[1]
        
            colorsM = rxs[1] + gxs[1] +bxs[1]
            finalString = finalString + "?&C1=" + colorsM
            count1 = count1 + 1
            rT = 0
            gT = 0
            bT = 0

            for y in range(0, 225, 5):
                for x in range(0, 360, 5):
                    r,g,b = image.getpixel((x, y))
                    rT = rT + r
                    gT = gT + g
                    bT = bT + b
                    count = count + 1

            
            rx = hex(int(rT/count))
            gx = hex(int(gT/count))
            bx = hex(int(bT/count))
        
            rxs = rx.split("x", 2)
            bxs = bx.split("x", 2)
            gxs = gx.split("x", 2)
            
            if(len(rxs[1]) == 1):
                crxs = ord(rxs[1])
                if((crxs >= 48 and  crxs <= 57) or (crxs >= 97 and  crxs <= 102)):
                    rxs[1] = "0" + rxs[1]
                    
            if(len(gxs[1]) == 1):
                cgxs = ord(gxs[1])
                if((cgxs >= 48 and  cgxs <= 57) or (cgxs >= 97 and  cgxs <= 102)):
                    gxs[1] = "0" + gxs[1]

            if(len(bxs[1]) == 1):
                cbxs = ord(bxs[1])
                if((cbxs >= 48 and  cbxs <= 57) or (cbxs >= 97 and  cbxs <= 102)):
                    bxs[1] = "0" + bxs[1]
            
            colorsM = rxs[1] + gxs[1] +bxs[1]
            finalString = finalString + "&C2=" + colorsM
            count1 = count1 + 1
            rT = 0
            gT = 0
            bT = 0

            for y in range(0, 225, 5):
                for x in range(1080, 1440, 5):
                    r,g,b = image.getpixel((x, y))
                    rT = rT + r
                    gT = gT + g
                    bT = bT + b
                    count = count + 1

            
            rx = hex(int(rT/count))
            gx = hex(int(gT/count))
            bx = hex(int(bT/count))
        
            rxs = rx.split("x", 2)
            bxs = bx.split("x", 2)
            gxs = gx.split("x", 2)
            
            if(len(rxs[1]) == 1):
                crxs = ord(rxs[1])
                if((crxs >= 48 and  crxs <= 57) or (crxs >= 97 and  crxs <= 102)):
                    rxs[1] = "0" + rxs[1]
                    
            if(len(gxs[1]) == 1):
                cgxs = ord(gxs[1])
                if((cgxs >= 48 and  cgxs <= 57) or (cgxs >= 97 and  cgxs <= 102)):
                    gxs[1] = "0" + gxs[1]

            if(len(bxs[1]) == 1):
                cbxs = ord(bxs[1])
                if((cbxs >= 48 and  cbxs <= 57) or (cbxs >= 97 and  cbxs <= 102)):
                    bxs[1] = "0" + bxs[1]
                
            colorsM = rxs[1] + gxs[1] +bxs[1]
            finalString = finalString + "&C3=" + colorsM
            count1 = count1 + 1

            for y in range(899, 675, -5):
                for x in range(1080, 1440, 5):
                    r,g,b = image.getpixel((x, y))
                    rT = rT + r
                    gT = gT + g
                    bT = bT + b
                    count = count + 1

            
            rx = hex(int(rT/count))
            gx = hex(int(gT/count))
            bx = hex(int(bT/count))
        
            rxs = rx.split("x", 2)
            bxs = bx.split("x", 2)
            gxs = gx.split("x", 2)
            
            if(len(rxs[1]) == 1):
                crxs = ord(rxs[1])
                if((crxs >= 48 and  crxs <= 57) or (crxs >= 97 and  crxs <= 102)):
                    rxs[1] = "0" + rxs[1]
                    
            if(len(gxs[1]) == 1):
                cgxs = ord(gxs[1])
                if((cgxs >= 48 and  cgxs <= 57) or (cgxs >= 97 and  cgxs <= 102)):
                    gxs[1] = "0" + gxs[1]

            if(len(bxs[1]) == 1):
                cbxs = ord(bxs[1])
                if((cbxs >= 48 and  cbxs <= 57) or (cbxs >= 97 and  cbxs <= 102)):
                    bxs[1] = "0" + bxs[1]
            
            colorsM = rxs[1] + gxs[1] +bxs[1]
            finalString = finalString + "&C4=" + colorsM
            count1 = count1 + 1

            req = requests.get('http://'+ ipD +'/'+ finalString)
            req.status_code
            #print(time.process_time())
            print(finalString)
            #print(count1)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=1001,debug=False)