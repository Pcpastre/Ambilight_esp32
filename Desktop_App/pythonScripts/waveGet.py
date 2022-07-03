import pyaudio
import numpy as np
from flask import Flask, request
from threading import *
import requests
import random

THREADS = []

app = Flask(__name__) 

maxValue = 2**16
bars = 35
p=pyaudio.PyAudio()

for i in range(p.get_device_count()):
    print(i, p.get_device_info_by_index(i)["name"])

stream=p.open(format=pyaudio.paInt16,channels=2,rate=44100,
              input=True,input_device_index=0, frames_per_buffer=1024)


class audioBars(Thread):
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
                        data = np.fromstring(stream.read(1024),dtype=np.int16)
                        dataL = data[0::2]
                        dataR = data[1::2]
                        peakL = np.abs(np.max(dataL)-np.min(dataL))/maxValue
                        peakR = np.abs(np.max(dataR)-np.min(dataR))/maxValue
                        print(peakL*100, peakR*100)
                        if((peakL*100) > 7 and (peakR*100) > 7):
                            rI =  random.randint(0, 255)
                            gI =  random.randint(0, 255)
                            bI =  random.randint(0, 255)
                            r = str(rI)
                            g = str(gI)
                            b = str(bI)
                            req = requests.get('http://'+ ipD +'/colorSend?R=' +r+ '&G=' +g+ '&B=' + b)
                            req.status_code
                        
                    except:
                        # Sometimes the APP stuck and this exception happens in a loop
                        print("Error in AudioBars")
                        self.alive  = False




@app.route('/Start', methods=["GET"])
def Start():
    
    ipDisp = request.args.get('ipDisp')

    m = audioBars(ipDisp)
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

    app.run(host='0.0.0.0', port=1000,debug=False)
