from operator import gt
from PIL import ImageGrab
import time
import numpy as np
from flask import Flask, request
from threading import *
import requests

THREADS = []

app = Flask(__name__) 





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
                        ipD = '192.168.0.102'
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


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=1001,debug=False)